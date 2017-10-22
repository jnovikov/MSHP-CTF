from flask import redirect
from flask import session

from app import app, admin, db
from app.models.db_models import User, Task, SolvedTask, Contest, ContestTask
from flask_admin.contrib.sqla import ModelView


class MyModelView(ModelView):
    column_editable_list = []

    def is_accessible(self):
        print(session)
        return session['login'] == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        print('why??')
        return redirect('/')


class ContestView(MyModelView):
    create_modal = True
    edit_modal = True
    column_editable_list = ['name', 'active', 'description']


class TaskModelView(MyModelView):
    create_modal = True
    edit_modal = True
    column_editable_list = ['name', 'cost', 'category', 'flag', 'file', 'active','desc']
    column_searchable_list = column_editable_list


class ContestTaskView(MyModelView):
    create_modal = True
    edit_modal = True


admin.add_view(MyModelView(User, db.session))
admin.add_view(TaskModelView(Task, db.session))
admin.add_view(MyModelView(SolvedTask, db.session))
admin.add_view(ContestView(Contest, db.session))
admin.add_view(ContestTaskView(ContestTask, db.session))
