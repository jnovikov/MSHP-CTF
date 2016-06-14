import json
from app.controllers.task_controller import add_task
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class TaskParser(object):
    category_map = {}
    tasks = []

    def __init__(self, filename):
        self.filename = os.path.join(basedir, filename)

    def load_task_from_file(self):
        with open(self.filename) as f:
            data = f.read()
            parsed_data = json.loads(data)
        self.tasks = parsed_data['tasks']

    def get_tasks(self):
        print(self.tasks)
        print(self.category_map)

    def add_task_to_db(self):
        for i in self.tasks:
            add_task(i)
