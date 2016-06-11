from app import db
from app.models.db_models import Task
from app.controllers.team_controller import solve_task, get_team_solved_tasks


def add_task(dictionary):
    _name = dictionary['name']
    task = Task.query.filter_by(name=_name).first()
    if task is not None:
        return task.id
    db.session.add(Task(**dictionary))
    db.session.commit()
    task = Task.query.filter_by(name=_name).first()
    return task.id


def check_flag(_id, team_id, flag):
    task = Task.query.filter_by(id=_id).first()
    solved = get_team_solved_tasks(team_id)
    cnt = solved.count(int(_id))
    if cnt != 0:
        return 'AlreadySolved'
    if task is None:
        return 'NotExist'
    if task.flag == flag:
        solve_task(team_id, task.id, task.cost)
        return "RightFlag"
    else:
        return "WrongFlag"


def get_task(_id):
    task = Task.query.filter_by(id=_id).first()
    if task is None:
        return False
    task = task.__dict__
    del task['_sa_instance_state']
    del task['flag']
    return task