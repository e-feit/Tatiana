import functools

import flask
from flask import render_template, Blueprint, Response

blueprint = Blueprint(__name__, __name__, template_folder='./templates', static_folder='assets')

def admin_only(f):
    @functools.wraps(f)
    def decorated_function(*args, **kws):
        from flask import current_app as app
        c = app.config
        token = flask.request.args.get('token')
        if not token:
            return render_template('error.html'), 401
        return f(*args, **kws)

    return decorated_function

@blueprint.route('/')
@admin_only
def admin():
    return render_template('admin.html')