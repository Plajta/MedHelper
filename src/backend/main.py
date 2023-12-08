from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user

app = Flask("PlajtaMed", template_folder='src/frontend/templates', static_url_path='/static', static_folder='src/frontend/static')

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        name = request.form['fname']
        lastname = request.form['lname']
        birth = request.form['birth']

        print(name)

    return render_template('admin.html', user="Damongus Veliký", position="Bůh všehomíra", auth="69")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/login', methods = ['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('admin'))
    return render_template('login.html', error=error)
