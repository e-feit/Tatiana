from flask import Flask, redirect
from flask_assets import Environment
from flask_login import LoginManager
from flask_migrate import Migrate
from webassets import Bundle

from app.db.models import db, User
from app.pages.home.home import blueprint as home_blueprint
from app.pages.login.login import blueprint as login_blueprint
from app.pages.planning.planning import blueprint as planning_blueprint
from app.pages.events.events import blueprint as events_blueprint
from app.pages.maintenance.maintenance import blueprint as maintenance_blueprint

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.static_folder = 'static'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/tatiana?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MAINTENANCE_MODE'] = True
    app.config['MAINTENANCE_TOKEN'] = 'abc'

    app.config['SECRET_KEY'] = 'some secret key'
    app.secret_key = app.config['SECRET_KEY']
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    # Здесь должны быть зарегистрированы все blueprints.
    # При создании нового, не забываем указать его здесь.
    app.register_blueprint(login_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(planning_blueprint)
    app.register_blueprint(events_blueprint)
    app.register_blueprint(maintenance_blueprint)

    db.init_app(app)
    login_manager.init_app(app)

    migrate = Migrate(app, db)

    assets = Environment(app)
    # assets.manifest = False
    # assets.cache = False
    # assets.auto_build = True
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

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@login_manager.unauthorized_handler
def handle_unauthorized():
    return redirect('/login')