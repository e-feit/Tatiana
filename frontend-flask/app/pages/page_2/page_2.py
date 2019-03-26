from flask import render_template, Blueprint
from flask_login import login_required

blueprint = Blueprint(__name__, __name__, template_folder='.', static_folder='assets')

@blueprint.route('/')
@login_required
def page_2():
    return render_template('page_2.html')