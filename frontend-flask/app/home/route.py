from flask import render_template, Blueprint

blueprint = Blueprint('home', __name__, template_folder='./templates', static_folder='assets')

@blueprint.route('/')
def home():
    return render_template('home.html')