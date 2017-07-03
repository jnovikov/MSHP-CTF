from flask import url_for
from app import db


class Contest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    active = db.Column(db.Boolean)
    contest_tasks = db.relationship("ContestTask", backref='Contest', lazy="dynamic")

    def __init__(self, name=''):
        self.name = name

    def get_link(self):
        return url_for('contest_view.contest_detail', c_id=self.id)

    def __repr__(self):
        return '<Contest {}>'.format(self.name)

    def is_active(self):
        return self.active


class ContestTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.Integer, db.ForeignKey("contest.id"))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    task = db.relationship('Task', uselist=False)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    cost = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String)
    desc = db.Column(db.String)
    file = db.Column(db.String)
    flag = db.Column(db.String)
    active = db.Column(db.Boolean)

    def __init__(self, cost=0, desc="", file="", flag="", category="", name="", active=True):
        self.cost = cost
        self.desc = desc
        self.file = file
        self.flag = flag
        self.category = category
        self.name = name
        self.active = active

    def __repr__(self):
        return '<Task {} {}-{}>'.format(self.name, self.category, self.cost)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    fio = db.Column(db.String)
    solved = db.Column(db.String)
    score = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    solved_tasks = db.relationship("SolvedTask", backref='User', lazy="dynamic")

    def __init__(self, login="", password="", fio=""):
        self.login = login
        self.password = password
        self.fio = fio
        self.score = 0
        self.active = True
        self.solved = " "

    def solve_task(self, task):
        self.score += task.cost
        self.solved += (' ' + str(task.id))

    def __repr__(self):
        return '<User {}>'.format(self.login)


class SolvedTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # user = db.relationship('User', uselist=False)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    task = db.relationship('Task', uselist=False)
    time = db.Column(db.String)

