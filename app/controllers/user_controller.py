from app import db
from app.controllers import TeamNotExist
from app.models.db_models import SolvedTask
from app.models.db_models import User
from app.time_tools import get_current_time


def get_user(_login):
    user = User.query.filter_by(login=_login).first()
    return user


def get_user_by_id(_id):
    user = User.query.filter_by(id=_id).first()
    return user


def check_user(login, password):
    user = User.query.filter_by(login=login, password=password).first()
    return user


def add_user(data):
    try:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
    except Exception as error:
        print(error)
        return False
    else:
        return True


def get_user_id(_login):
    user = User.query.filter_by(login=_login).first()
    if user is not None:
        return user.id


def get_team_solved_tasks(_id):
    user = User.query.filter_by(id=_id).first()
    if user is None:
        return TeamNotExist
    if user.solved is None:
        return []
    solved = user.solved.split()
    solved = list(map(int, solved))
    return solved


def solve_task(_id, task):
    user = User.query.filter_by(id=_id).first()
    if user is None:
        return TeamNotExist
    solved = SolvedTask()
    solved.task = task
    solved.user = user
    solved.time = get_current_time()
    user.solve_task(task)
    user.solved_tasks.append(solved)
    db.session.add(solved)
    db.session.commit()
    return True


def get_user_scores():
    return User.query.order_by(-User.score)
