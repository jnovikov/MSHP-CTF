from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect, CSRFProtect
from flask_admin import Admin


class FlaskWithTemplatesAutoReload(Flask):
    def create_jinja_environment(self):
        self.config['TEMPLATES_AUTO_RELOAD'] = True
        return Flask.create_jinja_environment(self)

app = FlaskWithTemplatesAutoReload(__name__)
limiter = Limiter(app, key_func=get_remote_address)

app.config.from_object('config')

csrf = CSRFProtect()
CSRFProtect(app)
csrf.init_app(app)

db = SQLAlchemy(app)
admin = Admin(app, name='CTF', template_mode='bootstrap3')
db.create_all()

from app.views.base_views import view
from app.views.contest_view import contest
from app.views import admin_view
app.register_blueprint(view)
app.register_blueprint(contest)
