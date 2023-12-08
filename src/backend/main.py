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
@login_required
def admin():
    if request.method == 'POST':
        displayname = request.form['displayname']
        rank = request.form['rank']
        level = request.form['level']

        #generate user id
        userid = uuid.uuid4()

    return render_template('admin.html', displayname=displayname, rank=rank, level=level)

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

        emit("patients-data", {"data": patient_array})

@socketio.on("delete-patient")
def handle_delete(data):
    print(data)