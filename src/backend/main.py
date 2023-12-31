from flask import Blueprint, render_template, request, flash, url_for, request, redirect, send_file
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from flask_socketio import SocketIO, emit
import uuid
from . import socketio
from .models import Patient, Doctor, Message, Placement, Questionnaire
from . import db
from datetime import date
import qrcode
import re
import os, shutil

main = Blueprint('main', __name__)


def genQR():
    pattern = "[^0-9a-zA-Z]+"
    if os.path.isdir("/tmp/medhelper"):
        shutil.rmtree("/tmp/medhelper")
    os.mkdir("/tmp/medhelper")
    print(Placement.query.all())
    for placement in Placement.query.all():
        img = qrcode.make(f'{url_for("main.app_first", _external=True)}?uuid={placement.id}')
        img.save(f"/tmp/medhelper/QR_{re.sub(pattern, '_', placement.placement)}.png")
    return shutil.make_archive("/tmp/medhelper_positions", "zip", "/tmp/medhelper")


def process_patients():
    patient_list = []

    for patient in Patient.query.all():
        patient_d = {}
        for column in patient.__table__.columns:
            patient_d[column.name] = str(getattr(patient, column.name))
        patient_list.append(patient_d)

    message_list = []

    for message in Message.query.all():
        if message.patient is not None and not message.response:
            message_d = {"name": message.patient.name, "uuid": message.user_id, "message": message.body}
            message_list.append(message_d)

    questions_list = []
    
    for questionnaire in Questionnaire.query.all():
        if questionnaire.patient is not None:
            question_d = {"name": questionnaire.patient.name, "uuid": questionnaire.user_id, "message": questionnaire.answers}
            questions_list.append(question_d)

    return patient_list, message_list, questions_list


def update_admin_frontend():
    patient_list, message_list, questions_list = process_patients()

    emit("patients-data", {
        "patients": patient_list,
        "messages": message_list,
        "questions": questions_list
    })


@main.route('/')
def app_first():
    uuid = request.args.get('uuid', default=None, type=str)
    if uuid == None:
        return render_template("response_client.html", code="401", message="nemáš oprávnění, špatné user info")
    username = Patient.query.filter_by(placement_id=uuid).first().name
    return render_template('app_first.html',username=username)


@main.route('/sec-init')
def app_second():
    uuid = request.args.get('uuid', default=None, type=str)
    if uuid == None:
        return render_template("response_client.html", code="401", message="nemáš oprávnění, špatné user info")
    print(uuid)
    uuid = uuid.split('?')[0]
    username = Patient.query.filter_by(placement_id=uuid).first().name
    return render_template('app_second.html',username=username)


@main.route('/third-init')
def app_third():
    uuid = request.args.get('uuid', default=None, type=str)
    if uuid == None:
        return render_template("response_client.html", code="401", message="nemáš oprávnění, špatné user info")

    return render_template('app_third.html')


@main.route('/home')
def app_home():
    uuid = request.args.get('uuid', default=None, type=str)
    if uuid == None:
        return render_template("response_client.html", code="401", message="nemáš oprávnění, špatné user info")

    return render_template('app_home.html')


@main.route('/chat')
def app_chat():
    uuid = request.args.get('uuid', default=None, type=str)
    if uuid == None:
        return render_template("response_client.html", code="401", message="nemáš oprávnění, špatné user info")

    # print(url_for("main.app", _external=True))
    return render_template('app_chat.html')


@main.route('/profile')
def app_profile():
    uuid = request.args.get('uuid', default=None, type=str)
    if uuid == None:
        return render_template("response_client.html", code="401", message="nemáš oprávnění, špatné user info")

    return render_template('app_user.html')


@main.route('/admin')
@login_required
def admin():
    displayname = current_user.displayname
    rank = current_user.rank
    level = current_user.level

    return render_template('admin.html', displayname=displayname, rank=rank, level=level, places=Placement.query.all())


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/download")
def download():
    path = genQR()

    return send_file(path, as_attachment=True)


#
# SOCKETIO ROUTES
#
@socketio.on("admin-event")
def handle_message_admin(data):
    if not isinstance(data, dict) or "command" not in data:
        return
    if data["command"] == "send-patients":
        update_admin_frontend()

    elif data["command"] == "patient-data":
        name = data["name"]
        birth = data["birth"]
        placement_id = data["space"]

        id = str(uuid.uuid4())

        new_patient = Patient(name=name, birth=birth, id=id, placement_id=placement_id)

        print(new_patient)

        db.session.add(new_patient)
        db.session.commit()

        update_admin_frontend()

    elif data["command"] == "delete-patient":
        db.session.delete(Patient.query.filter_by(id=data["uuid"]).first())
        db.session.commit()

    elif data["command"] == "response-send":
        body = data["body"]
        user_id = data["uuid"]
        timestamp = date.today()
        response = True
        patient = Patient.query.filter_by(id=user_id).first()

        new_message = Message(user_id=user_id, body=body, response=response, timestamp=timestamp, patient=patient)

        db.session.add(new_message)
        db.session.commit()

        update_admin_frontend()


@socketio.on("message-user-send")
def user_message(data):
    placement_id = data["uuid"]
    body = data["message"]
    response = False
    timestamp = date.today()
    patient = Patient.query.filter_by(placement_id=placement_id).first()
    if patient is not None:
        new_message = Message(user_id=patient.id, body=body, response=response, timestamp=timestamp, patient=patient)

        db.session.add(new_message)
        db.session.commit()

        update_admin_frontend()


@socketio.on("load-chat")
def load_chat(data):
    uuid = data["uuid"]

    message_list = []

    if data["type"] == "messages":
        for message in Message.query.filter_by(user_id=uuid):
            message_d = {"name": message.patient.name, "uuid": message.user_id, "message": message.body,
                         "response": message.response}
            message_list.append(message_d)
    emit("update-messages", message_list)

@socketio.on("load-chat-by-bed")
def load_chat_by_bed(data):
    placement_id = data["uuid"]

    message_list = []

    patient = Patient.query.filter_by(placement_id=placement_id).first()

    if data["type"] == "messages":
        for message in Message.query.filter_by(user_id=patient.id):
            message_d = {"name": message.patient.name, "uuid": message.user_id, "message": message.body,
                         "response": message.response}
            message_list.append(message_d)
    emit("update-messages", message_list)

@socketio.on("send-space")
def send_space(data):
    name = data

    id = str(uuid.uuid4())

    new_placement = Placement(id=id, placement=name)

    db.session.add(new_placement)
    db.session.commit()

@socketio.on("summary-data")
def handle_summary(data):
    placement_id = data["uuid"]
    data = data["data"]
    timestamp = date.today()

    patient = Patient.query.filter_by(placement_id=placement_id).first()

    new_questinnaire = Questionnaire(user_id=patient.id, answers=str(data), timestamp=timestamp, patient=patient)

    db.session.add(new_questinnaire)
    db.session.commit()

    update_admin_frontend()
    #1 - unhappy
    #2 - ...
    #3
    #4 - content
    #5 - happy
    #6 - extremely happy
