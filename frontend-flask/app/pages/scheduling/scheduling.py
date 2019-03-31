import json

from flask import render_template, Blueprint, request
from flask_login import login_required

from app.db.models import Scheduler, db

blueprint = Blueprint(__name__, __name__, template_folder='.')

SCHEDULER_TYPES = {
    '1': {'label': 'Пн-Пт'},
    '2': {'label': 'Сб-Вс'},
    '3': {'label': 'Пн-Вс', 'default_selected': True},
}

@blueprint.route('/scheduling')
@login_required
def index():
    return render_template('scheduling.html', scheduler_types = SCHEDULER_TYPES, schedulers = get_all_schedulers())


@blueprint.route('/scheduling', methods=['POST'])
@login_required
def add_scheduler_item():
    data = request.get_json(force=True)
    scheduler = Scheduler()
    scheduler.calendar = data['type']
    scheduler.ontime = data['start']
    scheduler.offtime = data['end']
    scheduler.pin = 1
    db.session.add(scheduler)
    db.session.flush()
    return ''

@blueprint.route('/scheduling/<int:item_id>', methods=['DELETE'])
@login_required
def delete_scheduler_item(item_id):
    return ''

def get_all_schedulers():
    return Scheduler.query.all()