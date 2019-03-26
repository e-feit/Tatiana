import functools

import flask
from flask import render_template, Blueprint, session

blueprint = Blueprint(__name__, __name__, template_folder='.', static_folder='assets')

def admin_only(f):
    @functools.wraps(f)
    def decorated_function(*args, **kws):
        from flask import current_app as app

        token = flask.request.args.get('token')
        mode = app.config['MAINTENANCE_MODE']
        maintenance_token = app.config['MAINTENANCE_TOKEN']

        if not token or not mode or (mode and token != maintenance_token):
            return render_template('error.html'), 401
        return f(*args, **kws)

    return decorated_function

@blueprint.route('/')
@admin_only
def admin():
    session['maintenance'] = True
    return render_template('admin.html')