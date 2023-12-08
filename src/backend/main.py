from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from flask_socketio import SocketIO, emit
import uuid
from . import socketio

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('main.html')


@main.route('/admin', methods=['POST', 'GET'])
#@login_required
def admin():
    if request.method == 'POST':
        name = request.form['fname']
        lastname = request.form['lname']
        birth = request.form['birth']

        #generate user id
        userid = uuid.uuid4()

    return render_template('admin.html', user="Amogus", position="Bůh všehomíra", auth="69")

@main.route("/about")
def about():
    return render_template("about.html")

#
# SOCKETIO ROUTES
#


@socketio.on("admin-event")
def handle_message_admin(data):
    if data == "send-patients":
        print("Send patients!")

        patient_array = [{
            "name": "františek hřímal",
            "desc": "Haha popis",
            "userid": "46154151a1f5a1sf3as"
        }]

        message_array = [{
            "name": "Žena #1",
            "message": "Yo nezavřeli jste okno a tak mi umrzly koule, fakt díky"
        },
        {
            "name": "Muž #1",
            "message": "Otevřete okno?"
        }]

        questions_array = [{
            "name": "Žena #1",
            "message": "Tato nemocnice se mi nelíbí, je cringe"
        },
        {
            "name": "Muž #1",
            "message": "Otevřete okno?"
        }]

        emit("patients-data", {
                "patients": patient_array,
                "messages": message_array,
                "questions": questions_array
            })

@socketio.on("delete-patient")
def handle_delete(data):
    print(data)