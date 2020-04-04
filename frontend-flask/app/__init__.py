import json
import os

from flask import Flask, redirect, jsonify
from flask_assets import Environment
from flask_login import LoginManager
from flask_migrate import Migrate
from webassets import Bundle

from app.db.models import db, User
from app.pages.home.home import blueprint as home_blueprint
from app.pages.login.login import blueprint as login_blueprint
from app.pages.scheduling.scheduling import blueprint as scheduling_blueprint
from app.pages.events.events import blueprint as events_blueprint
from app.pages.maintenance.maintenance import blueprint as maintenance_blueprint
from app.shared.tatiana_exception import TatianaException

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.static_folder = 'static'

    db_host = os.getenv('TATIANA_DB_HOST', '127.0.0.1')
    db_username = os.getenv('TATIANA_DB_USERNAME', 'root')
    db_password = os.getenv('TATIANA_DB_PASSWORD', '')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + db_username + ':' + db_password + '@' \
                                            + db_host +'/tatiana?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = 'some secret key'
    app.secret_key = app.config['SECRET_KEY']
    app.config['JSON_AS_ASCII'] = False

    # Здесь должны быть зарегистрированы все blueprints.
    # При создании нового, не забываем указать его здесь.
    app.register_blueprint(login_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(scheduling_blueprint)
    app.register_blueprint(events_blueprint)
    app.register_blueprint(maintenance_blueprint)


    db.init_app(app)
    login_manager.init_app(app)

    migrate = Migrate(app, db)

    assets = Environment(app)
    assets.url = app.static_url_path
    scss = Bundle(

        # здесь нужно указать все файлы .scss
        'scss/variables.scss',
        'scss/reset.scss',
        'scss/base.scss',
        'scss/navbar.scss',
        'scss/pages/login.scss',

        filters='pyscss', output='styles/style.css')

    assets.register('scss_all', scss)

    app.register_error_handler(TatianaException, handle_error_response)

    return app

def handle_error_response(error: TatianaException):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def handle_unauthorized():
    return redirect('/login')