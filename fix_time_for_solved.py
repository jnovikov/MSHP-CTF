from app import db
from app.models.db_models import SolvedTask
from datetime import datetime
for solved_task in SolvedTask.query.all():
    dt = datetime.strptime(solved_task.time, "%x %X")
    solved_task.time = dt.strftime("%Y-%m-%d %H:%M:%S")
    db.session.add(solved_task)
    db.session.commit()