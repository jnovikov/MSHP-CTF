from app.models.db_models import Team
from app import db


def get_team(_name):
    team = Team.query.filter_by(name=_name).first()
    return team


def get_team_id(_name):
    team = Team.query.filter_by(name=_name).first()
    if team is not None:
        return team.id


def create_team(_name):
    team = get_team(_name)
    if team is not None:
        return 'Team already exist'
    print('Adding team', _name)
    db.session.add(Team(_name))
    db.session.commit()
    return True


def get_team_solved_tasks(_id):
    team = Team.query.filter_by(id=_id).first()
    solved = team.solved.split()
    solved = list(map(int, solved))
    return solved


def solve_task(_id, task_id, task_score):
    team = Team.query.filter_by(id=_id).first()
    if team is None:
        return 'Team not exist'
    team.solve_task(task_id, task_score)
    db.session.commit()
    return True


def get_team_scores():
    team = Team.query.order_by(Team.score)
    team = team[::-1]
    return team
