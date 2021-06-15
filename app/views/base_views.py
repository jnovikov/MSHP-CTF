from collections import defaultdict

from flask import render_template, request, redirect, url_for, abort, Blueprint, flash

from app import limiter, app
from app.controllers.task_controller import get_task, check_flag, solved_task_query_builder, SubmitResult
from app.controllers.user_controller import add_user, check_user, get_user_scores, get_user_by_id, get_all_groups, \
    get_groups_builder, get_groups_with_user_info, add_user_to_the_group
from app.forms import LoginForm, RegisterForm
from app.login_tools import login_required, get_base_data, login_user, logout_user, user_id
from app.views import LogoutMessage

view = Blueprint('view', __name__, static_folder='static', template_folder='templates')


@view.route('/')
def index():
    context = get_base_data()
    return render_template('index.html', **context)


@view.route('/login', methods=['POST', 'GET'])
@limiter.limit("5 per second")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(form.data)
        del form['csrf_token']
        user = check_user(**form.data)
        if user is None:
            flash('Неправильный логин или пароль')
            return render_template('login.html', form=form)
        if app.config.get('CHECK_USER_ACTIVE', True) and not user.active:
            flash("Пользователь неактивен")
            return render_template('login.html', form=form)
        else:
            login_user(user)
            return redirect(url_for('contest_view.list_contests'))
    else:
        return render_template('login.html', form=form)


@view.route('/register', methods=['POST', 'GET'])
@limiter.limit("5 per second")
def register():
    form = RegisterForm()
    context = dict(form=form)
    if form.validate_on_submit():
        b = form.data
        del b['confirm']
        del b['csrf_token']
        flag = add_user(b)
        if flag:
            # login_user(get_user(form.login.data))
            return redirect('/login')
        else:
            flash('Произошла ошибка!Напишите Николаю или Ивану о ней!!!')
            return redirect('/register')
    else:
        return render_template('register.html', **context)


# @view.route('/tasks')
# @login_required
# def get_tasks():
#     context = get_base_data()
#     task_map = get_all_tasks()
#     if task_map is None:
#         task_map = {"No task": []}
#     context.update(task_map=task_map)
#     return render_template('tasks.html', **context)


@view.route('/task/<_id>', methods=['POST', 'GET'])
@limiter.limit("10 per second")
@login_required
def get_task_page(_id):
    context = get_base_data()
    task = get_task(_id)
    if not task or not task['active']:
        abort(404)
    contest_id = request.args.get('c_id', None)
    if request.method == 'GET':
        context.update(task)
        first_blood_users_show = app.config.get('FIRST_BLOOD_SHOW_COUNT', 3)
        context['solved'] = solved_task_query_builder((_id,)).limit(first_blood_users_show).all()
        return render_template('task_page.html', **context)
    else:
        usr_flag = request.form['flag']
        status = check_flag(_id, context['u_id'], usr_flag)
        context = get_base_data()
        back_url = request.url
        if (status == SubmitResult.OK or status == SubmitResult.ALREADY_SOLVED) and contest_id is not None:
            back_url = url_for('contest_view.contest_detail', c_id=contest_id)

        context['contest_id'] = contest_id
        context['back_url'] = back_url
        context.update(message=status.status_message(), )
        return render_template('message.html', **context)


@view.route('/task/<_id>/solvers')
@limiter.limit("10 per second")
@login_required
def get_solvers_page(_id):
    context = get_base_data()
    task = get_task(_id)
    if not task or not task['active']:
        abort(404)
    context.update(task)
    context['solved'] = solved_task_query_builder((_id,)).all()
    return render_template("solvers.html", **context)


@view.route('/logout')
def logout():
    logout_user()
    flash(LogoutMessage)
    return redirect(url_for('view.index'))


@view.route('/score')
def scoreboard(group_id=None):
    context = get_base_data()
    group_id = request.args.get("group_id")
    context.update(teams=get_user_scores(group_id=group_id))
    return render_template('scores.html', **context)


@view.route('/telegram')
def telegram():
    return "https://telegram.me/joinchat/BC2xhwdCtCCAQ7cbHymaSw"


@view.route('/user/<user_id>')
def user_view(user_id):
    context = get_base_data()
    user = get_user_by_id(user_id)
    context['user'] = user
    return render_template('user_page.html', **context)


@view.route('/report')
def report_view():
    return render_template('report.html')


@view.route('/groups')
def groups_view():
    context = get_base_data()
    groups = defaultdict(dict)
    for g in get_all_groups():
        groups[g.id]['group'] = g
        groups[g.id]['joined'] = False
    joined_groups = get_groups_with_user_info(user_id()).all()
    for g in joined_groups:
        groups[g.id]['joined'] = True
    context['groups'] = groups

    return render_template("groups.html", **context)


@view.route('/groups/<g_id>/join', methods=['POST', 'GET'])
def group_join_view(g_id):
    group = get_groups_builder().filter_by(id=g_id).first()
    if group is None:
        abort(404)
        return
    if request.method == 'GET':
        return render_template('join_group.html', group=group)
    add_user_to_the_group(group, user_id())
    return redirect(url_for('.groups_view'))

