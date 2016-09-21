from app import db, limiter
from app.models.db_models import Task
from app.controllers.user_controller import solve_task, get_team_solved_tasks


def add_task(dictionary):
    _name = dictionary['name']
    task = Task.query.filter_by(name=_name).first()
    if task is not None:
        return task.id
    db.session.add(Task(**dictionary))
    db.session.commit()
    task = Task.query.filter_by(name=_name).first()
    return task.id


@limiter.limit("1 per second")
def check_flag(_id, team_id, flag):
    task = Task.query.filter_by(id=_id).first()
    solved = get_team_solved_tasks(team_id)
    if int(_id) in solved:
        return 'Вы уже решили этот таск'
    if task is None:
        return 'Нет такого таска'
    if task.flag == flag:
        solve_task(team_id, task.id, task.cost)
        return "Правильно!"
    else:
        return "Неа :("


def get_task(_id):
    task = Task.query.filter_by(id=_id).first()
    if task is None:
        return False
    task = task.__dict__
    del task['_sa_instance_state']
    del task['flag']
    return task


def get_all_tasks():
    task = Task.query.all()
    task_map = {}
    for i in task:
        if i.category not in task_map.keys():
            task_map[i.category] = []
        task_map[i.category].append((i.id , i.cost))
    return task_map
