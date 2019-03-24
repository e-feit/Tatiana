from flask import Blueprint, render_template

mod = Blueprint('page-2', __name__, template_folder='templates', static_folder='assets')

@mod.route('/')
def page_2():
    return render_template('page_2/page_2.html')