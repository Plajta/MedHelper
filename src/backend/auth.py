from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Doctor
from . import db
import uuid

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    error = None
    info = None
    if request.args.get('logout'):
        info = "Úspěšně jsme Vás odhlásili"
    if request.args.get('wrong_cred'):
        error = "Špatné jméno nebo heslo"

    print(error)
    return render_template('login.html', error=error, info=info)


@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Doctor.query.filter_by(username=username).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login', wrong_cred=True))  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.admin'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():

    username = request.form.get('username')
    displayname = request.form.get('displayname')
    password = request.form.get('password')
    rank = request.form.get('rank')
    level = request.form.get('level')


    user = Doctor.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Username address already exists')
        return redirect(url_for('auth.signup'))

    id = str(uuid.uuid4())

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = Doctor(id=id ,username=username, displayname=displayname, password=generate_password_hash(password, method='pbkdf2'), rank=rank, level=level)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            displayname = request.form.get("displayname")
            rank = request.form.get("rank")
            level = request.form.get("level")

            user = Doctor.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database

            if user: # if a user is found, we want to redirect back to signup page so user can try again  
                flash('Username address already exists')
                #TODO: dodělat!
                print("Uživatel existuje")
                return redirect(url_for('auth.register'))

            id = str(uuid.uuid4())

            # create new user with the form data. Hash the password so plaintext version isn't saved.
            new_user = Doctor(id=id ,username=username, displayname=displayname, password=generate_password_hash(password, method='pbkdf2'), rank=rank, level=int(level))

            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            
        except Exception as err:
            print(err)
            return render_template("response.html", code="500", message="Internal server error")
        else:
            return render_template("response.html", code="200", message="Operation successful")


    if current_user.level == 0:
        return render_template("register.html")
    else:
        return render_template("response.html", code="401", message="Operation not permitted")
    
@auth.route("/register-space", methods=['GET', 'POST'])
def register_space():
    if request.method == "POST":
        bed_name = request.form.get("space")
        print(bed_name)

    if current_user.level == 0:
        return render_template("register_space.html")
    else:
        return render_template("response.html", code="401", message="Operation not permitted")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login', logout=True))
