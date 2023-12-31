
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO, emit
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
socketio = SocketIO()

def create_app():
    app = Flask(__name__,
                template_folder='../frontend/templates',
                static_url_path='/static',
                static_folder='../frontend/static')
    current_working_directory = os.getcwd()

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(current_working_directory,'db.sqlite')}"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Doctor

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Doctor.query.get(user_id)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
