from import_tasks import TaskParser

t = TaskParser('tasks.json')
t.load_task_from_file()
t.create_category_map()

task_map = t.category_map
