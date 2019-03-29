from flask import render_template, Blueprint, redirect, flash
from flask_login import login_user, login_required, current_user, logout_user

from app import User
from app.pages.login.login_form import LoginForm

blueprint = Blueprint(__name__, __name__, template_folder='.')

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Если юзер уже и так залогинен, то редиректим на главную
    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        login_field = form.login
        password_field = form.password

        user = User.query.filter_by(login = login_field.data).first()
        if user and user.password == password_field.data:
            login_user(user)
            return redirect('/')
        else:
            flash('Неверный логин или пароль!', 'error')

    return render_template('login.html', title='Sign In', form=form)

@blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login')