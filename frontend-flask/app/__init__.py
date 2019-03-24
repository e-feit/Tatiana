from flask import Flask

from .home.views import mod as home_blueprint
from .page_2.views import mod as page_2_blueprint

def create_app():
    app = Flask(__name__)
    app.static_folder = 'assets'

    app.register_blueprint(home_blueprint)
    app.register_blueprint(page_2_blueprint, url_prefix="/page-2")

    return app