from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

app.config.from_object('config')

csrf = CsrfProtect()
CsrfProtect(app)
csrf.init_app(app)

db = SQLAlchemy(app)

db.create_all()

from app.views.base_views import view

app.register_blueprint(view)

