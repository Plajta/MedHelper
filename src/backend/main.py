from flask import Blueprint, render_template, request, flash, url_for, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from flask_socketio import SocketIO, emit
import uuid
from . import socketio
from .models import Patient, Doctor, Message, Placement
from . import db
from datetime import date
import qrcode
import re
import os, shutil

main = Blueprint('main', __name__)


def genQR():
    pattern = "[^0-9a-zA-Z]+"
    shutil.rmtree("/tmp/medhelper")
    os.mkdir("/tmp/medhelper")
    for placement in Placement.query.all():
        img = qrcode.make(f'{url_for("main.app", _external=True)}?uuid={placement.id}')
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
        message_d = {"name": message.patient.name, "uuid": message.user_id, "message": message.body}
        message_list.append(message_d)

    questions_list = [{
        "name": "Žena #1",
        "uuid": "nbknakgmaů",
        "message": "Tato nemocnice se mi nelíbí, je cringe"
    },
        {
            "name": "Muž #1",
            "uuid": "najkkgnal",
            "message": "Otevřete okno?"
        }]

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
    uuid = request.args.get('uuid', default = None, type = str)
    #username = Patient.query.filter_by(id=uuid).first().name
    #TODO: load username!
    return render_template('app_first.html')


@main.route('/sec-init')
def app_second():
    return render_template('app_second.html')


@main.route('/third-init')
def app_third():
    return render_template('app_third.html')


@main.route('/home')
def app_home():
    return render_template('app_home.html')


@main.route('/chat')
def app_chat():
    #print(url_for("main.app", _external=True))
    return render_template('app_chat.html')


@main.route('/profile')
def app_profile():
    return render_template('app_user.html')


@main.route('/admin')
@login_required
def admin():
    displayname = current_user.displayname
    rank = current_user.rank
    level = current_user.level

    return render_template('admin.html', displayname=displayname, rank=rank, level=level)


@main.route("/about")
def about():
    return render_template("about.html")


#
# SOCKETIO ROUTES
#
@socketio.on("admin-event")
def handle_message_admin(data):
    if not isinstance(data, dict) and "command" in data:
        return
    if data["command"] == "send-patients":
        update_admin_frontend()

    elif data["command"] == "patient-data":
        name = data["name"]
        birth = data["birth"]
        placement = data["space"]

        id = str(uuid.uuid4())

        new_patient = Patient(name=name, birth=birth, id=id)

        print(new_patient)

        db.session.add(new_patient)
        db.session.commit()

        update_admin_frontend()

    elif data["command"] == "delete-patient":
        db.session.delete(Patient.query.filter_by(id=data["uuid"]).first())
        db.session.commit()

    elif data["command"] == "message-send":
        body = data["body"]
        timestamp = date.fromtimestamp()

        new_message = Message()


@socketio.on("message-user-send")
def user_message(data):
    user_id = data["uuid"]
    body = data["message"]
    response = False
    timestamp = date.today()
    patient = Patient.query.filter_by(id=user_id).first()

    new_message = Message(user_id=user_id, body=body, response=response, timestamp=timestamp, patient=patient)

    db.session.add(new_message)
    db.session.commit()

    update_admin_frontend()


@socketio.on("load-chat")
def load_chat(data):
    uuid = data["uuid"]
    
    message_list = []

    if data["type"] == "messages":
        for message in Message.query.all():
            message_d={"name": message.patient.name, "uuid": message.user_id, "message": message.body}
            message_list.append(message_d)
    emit("update-messages", message_list)
