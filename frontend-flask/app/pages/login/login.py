from flask import render_template, Blueprint, redirect, flash
from flask_login import login_user, login_required, current_user, logout_user
from argon2 import PasswordHasher
from datetime import datetime

from app import User, db
from app.pages.login.login_form import LoginForm

blueprint = Blueprint(__name__, __name__, template_folder='.')

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Если юзер уже и так залогинен, то редиректим на главную
    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data

        # если таблица юзеров пустая и юзер с логином 'admin'
        # пытается залогиниться, то создадим его
        if login == 'admin' and User.query.count() == 0:
            create_admin()

        user = User.query.filter_by(login = login).first()
        password_hasher = PasswordHasher()
        if user and password_hasher.verify(user.password, password):
            login_user(user)
            user.last_login = datetime.now()
            db.session.add(user)
            db.session.flush()
            return redirect('/')
        else:
            flash('Неверный логин или пароль!', 'error')

    return render_template('login.html', title='Sign In', form=form)

@blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login')

def create_admin():
    password_hasher = PasswordHasher()
    user = User()
    user.login = 'admin'
    user.password = password_hasher.hash('admin')
    user.username = 'Admin'
    db.session.add(user)