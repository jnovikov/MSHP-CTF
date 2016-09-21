from app import db
from app.models.db_models import User
from app.controllers import SuccessfulLogin, TeamAddedMessage, TeamNotExist


def get_user(_login):
    user = User.query.filter_by(login=_login).first()
    return user


def check_user(login,password):
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
    solved = user.solved.split()
    solved = list(map(int, solved))
    return solved


def solve_task(_id, task_id, task_score):
    user = User.query.filter_by(id=_id).first()
    if user is None:
        return TeamNotExist
    user.solve_task(task_id, task_score)
    db.session.commit()
    return True


def get_user_scores():
    return User.query.order_by(-User.score)
