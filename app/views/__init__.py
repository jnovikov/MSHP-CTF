from app.controllers.task_controller import get_all_tasks

try:
    task_map = get_all_tasks()
except Exception:
    task_map = {"No task": []}


LogoutMessage = 'Вы успешно вышли'


