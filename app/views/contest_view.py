from flask import Blueprint, render_template, abort

from app import limiter
from app.controllers.contest_controller import get_contests_list
from app.controllers.task_controller import get_tasks_by_contest_id
from app.login_tools import get_base_data
from app.models.db_models import Contest

contest = Blueprint('contest_view', __name__, static_folder='static', template_folder='templates', url_prefix='/contests')


@contest.route('/')
@limiter.limit("10 per second")
def list_contests():
    context = get_base_data()
    context.update(dict(contests=get_contests_list()))
    return render_template('contests.html', **context)


@contest.route('/<c_id>')
@limiter.limit("10 per second")
def contest_detail(c_id):
    context = get_base_data()
    curr_contest = Contest.query.get(int(c_id))
    if not curr_contest.is_active():
        abort(404)
    task_map = get_tasks_by_contest_id(curr_contest)
    context.update(task_map=task_map)
    context.update(contest_id=c_id)
    return render_template('tasks.html', **context)

# @contest.route('/<c_id>/score')
# @limiter.limit("10 per second")
# def contest_score(c_id):
#     context = get_base_data()
#     curr_contest = Contest.query.get(int(c_id))
#     if not curr_contest.is_active():
#         abort(404)
