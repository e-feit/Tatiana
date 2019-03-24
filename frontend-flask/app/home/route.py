from flask import render_template, Blueprint

blueprint = Blueprint(__name__, __name__, template_folder='.', static_folder='assets')

@blueprint.route('/')
def home():
    return render_template('home.html')