
from app.models.db_models import Contest


def get_contests_list():
    return Contest.query.filter_by(active=True).all()
