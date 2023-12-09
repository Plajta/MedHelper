from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from flask_socketio import SocketIO, emit
import uuid
from . import socketio
from .models import Patient, Doctor
from . import db
from .userapp import UserApp
main = Blueprint('main', __name__)


userApp = UserApp()

def process_patients():
    patient_list = []

    for patient in Patient.query.all():
        patient_d={}
        for column in patient.__table__.columns:
            patient_d[column.name] = str(getattr(patient, column.name))
        patient_list.append(patient_d)

    message_list = [{
        "name": "Žena #1",
        "uuid": "abgjakgb",
        "message": "Yo nezavřeli jste okno, fakt díky"
    },
    {
        "name": "Muž #1",
        "uuid": "anjgkanklg",
        "message": "Otevřete okno?"
    }]

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

@main.route('/')
def index():
    return render_template('main.html')

@main.route('/app')
def shitApp():
    userApp.returnWeb()

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
    if not isinstance(data, dict):
        return
    if data["command"] == "send-patients":
        patient_list, message_list, questions_list = process_patients()

        emit("patients-data", {
            "patients": patient_list,
            "messages": message_list,
            "questions": questions_list
        })

    elif data["command"] == "patient-data":
        name = data["name"]
        birth = data["birth"]

        id = str(uuid.uuid4())

        new_patient = Patient(name=name, birth=birth, id=id)

        db.session.add(new_patient)
        db.session.commit()

        patient_list, message_list, questions_list = process_patients()

        emit("patients-data", {
                "patients": patient_list,
                "messages": message_list,   
                "questions": questions_list
        })
    
    elif data["command"] == "delete-patient":
        db.session.delete(Patient.query.filter_by(id=data["uuid"]).first())
        db.session.commit()

    elif data["command"] == "message-send":
        print(data["body"])