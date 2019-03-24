from flask import Flask
from flask_migrate import Migrate

from app.db.models import db
from .home.route import blueprint as home_blueprint
from .page_2.route import blueprint as page_2_blueprint
from .maintenance.route import blueprint as maintenance_blueprint

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
        app.logger.warn('Maintenance mode is active! ' + 'You can access it under: /maintenance/?token=' + app.config['MAINTENANCE_TOKEN'])

    # Здесь должны быть зарегистрированы все blueprints.
    # При создании нового, не забываем указать его здесь.
    app.register_blueprint(home_blueprint)
    app.register_blueprint(page_2_blueprint, url_prefix = '/page-2')
    app.register_blueprint(maintenance_blueprint, url_prefix ='/maintenance')

    db.init_app(app)

    migrate = Migrate(app, db)

    return app