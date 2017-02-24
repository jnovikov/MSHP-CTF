from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    cost = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String)
    desc = db.Column(db.String)
    file = db.Column(db.String)
    flag = db.Column(db.String)

    def __init__(self, cost=0, desc="", file="", flag="", category="", name=""):
        self.cost = cost
        self.desc = desc
        self.file = file
        self.flag = flag
        self.category = category
        self.name = name

    def __repr__(self):
        return '<Task %r>' % self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    fio = db.Column(db.String)
    solved = db.Column(db.String)
    score = db.Column(db.Integer)
    solved_tasks = db.relationship("SolvedTask", backref='User', lazy="dynamic")

    def __init__(self, login="", password="", fio=""):
        self.login = login
        self.password = password
        self.fio = fio
        self.score = 0
        self.solved = ""

    def solve_task(self, task):
        self.score += task.cost
        self.solved += (' ' + str(task.id))


class SolvedTask(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    task = db.relationship('Task', uselist=False)
    time = db.Column(db.String)

    def __init__(self):
        pass
