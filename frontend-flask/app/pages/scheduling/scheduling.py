import json
import re

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

    start = data['start']
    end = data['end']
    type = data['end']

    if not is_time_valid(start) or not is_time_valid(end):
        return json.dumps({
            'error': True,
            'message': 'Некорректный формат времени (hh:mm:ss)'
        }, ensure_ascii=False), 400

    scheduler = Scheduler()
    scheduler.calendar = type
    scheduler.ontime = start
    scheduler.offtime = end
    scheduler.pin = 1
    db.session.add(scheduler)
    db.session.flush()

    return json.dumps({}), 201

@blueprint.route('/scheduling/<int:item_id>', methods=['DELETE'])
@login_required
def delete_scheduler_item(item_id):
    return ''

def get_all_schedulers():
    return Scheduler.query.all()

def is_time_valid(time):
    pattern = '^(\d{2}):(\d{2}):(\d{2})$'
    matches = re.search(pattern, time)

    if not matches:
        return False

    hours = int(matches.group(1))
    minutes = int(matches.group(2))
    seconds = int(matches.group(3))

    if hours > 23 or minutes > 59 or seconds > 59:
        return False

    return True