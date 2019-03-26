from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from app.db.models import db, User
from app.pages.home.route import blueprint as home_blueprint
from app.pages.page_2.route import blueprint as page_2_blueprint
from app.pages.maintenance.route import blueprint as maintenance_blueprint

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.static_folder = 'assets'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/tatiana?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MAINTENANCE_MODE'] = True
    app.config['MAINTENANCE_TOKEN'] = 'abc'

    app.config['SECRET_KEY'] = 'some secret key'
    app.secret_key = app.config['SECRET_KEY']

    if app.config['MAINTENANCE_MODE']:
        app.logger.info('Maintenance mode is active! ' + 'You can access it under: /maintenance/?token=' + app.config['MAINTENANCE_TOKEN'])

    # Здесь должны быть зарегистрированы все blueprints.
    # При создании нового, не забываем указать его здесь.
    app.register_blueprint(home_blueprint)
    app.register_blueprint(page_2_blueprint, url_prefix = '/page-2')
    app.register_blueprint(maintenance_blueprint, url_prefix ='/maintenance')

    db.init_app(app)
    login_manager.init_app(app)

    migrate = Migrate(app, db)

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()