from flask import render_template, Blueprint
from flask_login import login_required

blueprint = Blueprint(__name__, __name__, template_folder='.')

@blueprint.route('/events')
@login_required
def index():
    return render_template('events.html')