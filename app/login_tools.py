from functools import wraps

from flask import session, flash, redirect, url_for
from app.controllers.user_controller import get_team_solved_tasks, get_user_scores, get_user_id


def loggedin():
    return 'login' in session


def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if loggedin():
            return function(*args, **kwargs)
        else:
            flash('Нужно залогиниться перед этим запросом')
            return redirect(url_for('view.login'))

    return decorated_function


def login_user(user):
    session['login'] = user.login
    t_id = user.id
    session['u_id'] = t_id
    session['solved'] = user.solved


def logout_user():
    session.clear()


def get_base_data():
    response = {'loggedin': loggedin()}
    if loggedin():
        response['login'] = session['login']
        t_id = session['u_id']
        response['u_id'] = t_id
        response['solved'] = get_team_solved_tasks(t_id)
    return response
