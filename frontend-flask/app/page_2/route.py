from flask import render_template, Blueprint

blueprint = Blueprint('page-2', __name__, template_folder='./templates', static_folder='assets')

@blueprint.route('/')
def page_2():
    return render_template('page_2.html')