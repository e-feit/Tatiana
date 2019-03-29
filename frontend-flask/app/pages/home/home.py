from flask import render_template, Blueprint
from flask_login import login_user, login_required

from app.db.models import User

blueprint = Blueprint(__name__, __name__, template_folder='.')

@blueprint.route('/')
@login_required
def index():
    return render_template('home.html')