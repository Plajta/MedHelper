from flask import Flask, render_template, redirect, request
from flask_socketio import SocketIO, emit

app = Flask("PlajtaMed", template_folder='src/frontend/templates', static_url_path='/static', static_folder='src/frontend/static')
socketio = SocketIO(app)

#
# APP ROUTES
#

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        name = request.form['fname']
        lastname = request.form['lname']
        birth = request.form['birth']


        #update admin windows

    return render_template('admin.html', user="Damongus Veliký", position="Bůh všehomíra", auth="69")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user == "amogus" and pwd == "ballz":
            return redirect("admin")
        return "Blbečku!"
    else:
        return render_template('login.html')
    


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

if __name__ == "__main__":
    socketio.run(app, allow_unsafe_werkzeug=True)