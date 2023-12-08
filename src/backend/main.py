from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from flask_socketio import SocketIO, emit
from . import socketio

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('main.html')


@main.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    if request.method == 'POST':
        name = request.form['fname']
        lastname = request.form['lname']
        birth = request.form['birth']

    return render_template('admin.html', user=current_user.name, position="Bůh všehomíra", auth="69")


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
            "desc": "Haha popis"
        }]

        emit("patients-data", {"data": patient_array})
