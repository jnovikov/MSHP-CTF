from flask import redirect
from flask import session

from app import app, admin, db
from app.models.db_models import User, Task, SolvedTask, Contest, ContestTask
from flask_admin.contrib.sqla import ModelView


class MyModelView(ModelView):
    def is_accessible(self):
        print(session)
        return session['login'] == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        print('why??')
        return redirect('/')


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Task, db.session))
admin.add_view(MyModelView(SolvedTask, db.session))
admin.add_view(MyModelView(Contest, db.session))
admin.add_view(MyModelView(ContestTask, db.session))
