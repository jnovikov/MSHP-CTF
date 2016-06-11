from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    cost = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String)
    desc = db.Column(db.String)
    file = db.Column(db.String)
    flag = db.Column(db.String)

    def __init__(self, cost, desc, file, flag, category, name):
        self.cost = cost
        self.desc = desc
        self.file = file
        self.flag = flag
        self.category = category
        self.name = name

    def __repr__(self):
        return '<Task %r>' % self.name


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    score = db.Column(db.Integer, nullable=False)
    solved = db.Column(db.String)

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.solved = ""

    def solve_task(self, task_id, task_score):
        self.score += task_score
        self.solved += (' '+str(task_id))
