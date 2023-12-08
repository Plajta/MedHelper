from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from flask_socketio import SocketIO, emit
import uuid
from . import socketio
from .models import Patient
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('main.html')


@main.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    if request.method == 'POST':
        name = request.form['name']
        birth = request.form['birth']

        id = str(uuid.uuid4())

        new_patient = Patient(name=name, birth=birth, id=id)

        db.session.add(new_patient)
        db.session.commit()


    displayname = current_user.displayname
    rank = current_user.rank
    level = current_user.level

    return render_template('admin.html', displayname=displayname, rank=rank, level=level)

@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            name = request.form["name"]
            level = request.form["level"]

            #TODO: log to database
            
        except Exception as err:
            return render_template("response.html", code="500", message="Internal server error")
        else:
            return render_template("response.html", code="200", message="Operation successful")


    if current_user.level == 0:
        return render_template("register.html")
    else:
        return "401 - Operation not permitted", 401

#
# SOCKETIO ROUTES
#


@socketio.on("admin-event")
def handle_message_admin(data):
    if data == "send-patients":
        print("Send patients!")

        patient_list = []

        for patient in Patient.query.all():
            patient_d={}
            for column in patient.__table__.columns:
                patient_d[column.name] = str(getattr(patient, column.name))
            patient_list.append(patient_d)

        message_list = [{
            "name": "Žena #1",
            "message": "Yo nezavřeli jste okno, fakt díky"
        },
        {
            "name": "Muž #1",
            "message": "Otevřete okno?"
        }]

        questions_list = [{
            "name": "Žena #1",
            "message": "Tato nemocnice se mi nelíbí, je cringe"
        },
        {
            "name": "Muž #1",
            "message": "Otevřete okno?"
        }]

        emit("patients-data", {
                "patients": patient_list,
                "messages": message_list,
                "questions": questions_list
            })

@socketio.on("delete-patient")
def handle_delete(data):
    db.session.delete(Patient.query.filter_by(id=data).first())
    db.session.commit()