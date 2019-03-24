from flask import Blueprint, render_template

mod = Blueprint('home', __name__, template_folder='templates', static_folder='assets')

@mod.route('/')
def home():
    return render_template('home/home.html')