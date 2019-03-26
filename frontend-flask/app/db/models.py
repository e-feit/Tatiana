from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={'autocommit': True})

# Здесь все модели, соответствующие таблицам в БД.
# Любое изменение нужно будет обновить в миграциях (см. README).

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), nullable=True)
    last_login = db.Column(db.DateTime(), nullable=True)

    # Эти методы нужны для Flask-Login
    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
