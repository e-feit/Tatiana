from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={'autocommit': True})

# Здесь все модели, соответствующие таблицам в БД.
# Любое изменение нужно будет обновить в миграциях (см. README).

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), nullable=True)
    last_login = db.Column(db.DateTime(), nullable=True)

class Scheduler(db.Model):
    __tablename__ = 'plan'

    id = db.Column(db.Integer, primary_key=True, comment='id строки плана')
    pin = db.Column(db.SmallInteger, nullable=False, comment='выходной пин')
    ontime = db.Column(db.CHAR(255), nullable=False, comment='время включения (hh:mm:ss)')
    offtime = db.Column(db.CHAR(255), nullable=False, comment='время выключения (hh:mm:ss)')
    calendar = db.Column(db.CHAR(255), nullable=False, default='3', comment='1-будни, 2-выхи, 3-ежедневно')