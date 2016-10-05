from flask import render_template, request, redirect, url_for, abort, Blueprint, flash

from app.controllers.task_controller import get_task, check_flag, get_all_tasks
from app.controllers.user_controller import add_user, check_user, get_user_scores, get_user
from app.login_tools import login_required, get_base_data, login_user, logout_user
from app.views import task_map, LogoutMessage
from app.forms import LoginForm, RegisterForm

view = Blueprint('view', __name__, static_folder='static', template_folder='templates')

task_map = task_map


@view.route('/')
def index():
    context = get_base_data()
    return render_template('index.html', **context)


@view.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.data)
        user = check_user(**form.data)
        if user is None:
            flash('Неправильный логин или пароль')
            return render_template('login.html', form=form)
        else:
            login_user(user)
            return redirect(url_for('view.get_tasks'))
    else:
        return render_template('login.html', form=form)


@view.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    context = dict(form=form)
    if form.validate_on_submit():
        b = form.data
        del b['confirm']
        print(b)
        flag = add_user(b)
        if flag:
            login_user(get_user(form.login.data))
            return redirect(url_for('view.get_tasks'))
        else:
            flash('Произошла ошибка!Напишите Николаю или Ивану о ней!!!')
            return redirect('/register')
    else:
        return render_template('register.html', **context)


@view.route('/tasks')
@login_required
def get_tasks():
    context = get_base_data()
    context.update(task_map=task_map)
    return render_template('tasks.html', **context)


@view.route('/task/<_id>', methods=['POST', 'GET'])
@login_required
def get_task_page(_id):
    context = get_base_data()
    task = get_task(_id)
    if task is False:
        abort(404)
    if request.method == 'GET':
        context.update(task)
        return render_template('task_page.html', **context)
    else:
        usr_flag = request.form['flag']
        message = check_flag(_id, context['t_id'], usr_flag)
        context = get_base_data()
        context.update(message=message)
        return render_template('message.html', **context)


@view.route('/logout')
def logout():
    logout_user()
    flash(LogoutMessage)
    return redirect(url_for('view.index'))


@view.route('/score')
def scoreboard():
    context = get_base_data()
    context.update(teams=get_user_scores())
    return render_template('scores.html', **context)


@view.route('/telegram')
def telegram():
    return "https://telegram.me/joinchat/BC2xhwdCtCCAQ7cbHymaSw"
