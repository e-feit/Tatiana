import flask
from flask import render_template, Blueprint
from flask_login import login_user

from app.db.models import User

blueprint = Blueprint(__name__, __name__, template_folder='.', static_folder='assets')

@blueprint.route('/')
def home():
    user = User.query.filter_by(login='eugen').first()
    login_user(user)
    return render_template('home.html')