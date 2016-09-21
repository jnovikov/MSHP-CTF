from functools import wraps

from flask import session, flash, redirect, url_for
from app.controllers.team_controller import get_team_solved_tasks, get_team_id


def loggedin():
    return 'team' in session


def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if loggedin():
            return function(*args, **kwargs)
        else:
            flash('Нужно залогиниться перед этим запросом')
            return redirect(url_for('view.login'))

    return decorated_function


def login_user(team_name):
    session['team'] = team_name
    t_id = get_team_id(team_name)
    session['t_id'] = t_id
    session['solved'] = get_team_solved_tasks(t_id)


def logout_user():
    session.pop('team', None)
    session.pop('t_id', None)
    session.pop('solved', None)


def get_base_data():
    response = {'loggedin': loggedin()}
    if loggedin():
        response['team_name'] = session['team']
        t_id = session['t_id']
        response['t_id'] = t_id
        response['solved'] = get_team_solved_tasks(t_id)
    return response
