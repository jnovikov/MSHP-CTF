from app import app

from import_tasks import TaskParser

t = TaskParser('tasks.json')
t.load_task_from_file()
t.add_task_to_db()

app.run(port=5000, debug=True)
