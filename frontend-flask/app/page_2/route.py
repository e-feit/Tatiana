from flask import render_template, Blueprint

blueprint = Blueprint(__name__, __name__, template_folder='.', static_folder='assets')

@blueprint.route('/')
def page_2():
    return render_template('page_2.html')