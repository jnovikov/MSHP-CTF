from app import db, limiter
from app.models.db_models import Task, Contest, ContestTask, SolvedTask
from app.controllers.user_controller import solve_task, get_team_solved_tasks
from sqlalchemy import func
from collections import defaultdict


def add_task(dictionary):
    _name = dictionary['name']
    task = Task.query.filter_by(name=_name).first()
    if task is not None:
        return task.id
    db.session.add(Task(**dictionary))
    db.session.commit()
    task = Task.query.filter_by(name=_name).first()
    return task.id


def check_flag(_id, u_id, flag):
    task = Task.query.filter_by(id=_id).first()
    solved = get_team_solved_tasks(u_id)
    if int(_id) in solved:
        return 'Вы уже решили этот таск'
    if task is None:
        return 'Нет такого таска'
    if task.flag == flag:
        solve_task(u_id, task)
        return "Правильно!"
    else:
        return "Неа :("


def get_task(_id):
    task = Task.query.filter_by(id=_id).first()
    if task is None:
        return None
    task = task.__dict__
    del task['_sa_instance_state']
    del task['flag']
    return task


def get_solved_task_builder(task_ids, sort=True):
    query = SolvedTask.query.filter(SolvedTask.task_id.in_(task_ids))
    if sort:
        query = query.order_by(SolvedTask.time)
    return query


def get_tasks_by_contest_id(contest):
    try:
        tasks = Task.query.filter_by(active=True). \
            join(Contest.contest_tasks). \
            filter(Contest.id == contest.id). \
            all()

        task_ids = [task.id for task in tasks]

        solved_tasks = get_solved_task_builder(task_ids, sort=False). \
            add_columns(func.count(SolvedTask.id)). \
            group_by(SolvedTask.task_id)

        solved_tasks = {solved.task_id: solves_num for solved, solves_num in solved_tasks}

    except AttributeError:
        return None
    else:
        return get_task_map(tasks, solved_tasks)


def get_task_map(task, solve_map):
    task_map = defaultdict(list)
    for i in task:
        solves = solve_map.get(i.id) or 0
        task_map[i.category].append({'id': i.id, 'cost': i.cost, 'solves_num': solves})
    return task_map
