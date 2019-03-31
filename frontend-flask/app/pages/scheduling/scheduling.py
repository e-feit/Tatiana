import json
import re

from flask import render_template, Blueprint, request
from flask_login import login_required

from app.shared.tatiana_exception import TatianaException
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

    start = validate_time(data['start'])
    end = validate_time(data['end'])
    type = data['end']

    scheduler = Scheduler()
    scheduler.calendar = type
    scheduler.ontime = start
    scheduler.offtime = end
    scheduler.pin = 1
    db.session.add(scheduler)
    db.session.flush()

    return json.dumps({}), 201

@blueprint.route('/scheduling/all')
@login_required
def all_schedulers():
    return json.dumps(Scheduler.serialize_list(get_all_schedulers()))

@blueprint.route('/scheduling/<int:item_id>', methods=['DELETE'])
@login_required
def delete_scheduler_item(item_id):
    return ''

def get_all_schedulers():
    return Scheduler.query.all()

def validate_time(time):
    pattern = '^(\d{2}):(\d{2}):(\d{2})$'
    matches = re.search(pattern, time)

    exception = TatianaException('Некорректный формат времени  (hh:mm:ss)')

    if not matches:
        raise exception

    hours = int(matches.group(1))
    minutes = int(matches.group(2))
    seconds = int(matches.group(3))

    if hours > 23 or minutes > 59 or seconds > 59:
        raise exception

    return time
