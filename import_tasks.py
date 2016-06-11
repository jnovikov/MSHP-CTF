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

    def create_category_map(self):
        for i in self.tasks:
            if i['category'] not in self.category_map.keys():
                self.category_map[i['category']] = []
            t = (add_task(i), i['cost'])
            self.category_map[i['category']].append(t)
