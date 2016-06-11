from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect

app = Flask(__name__)

app.config.from_object('config')

csrf = CsrfProtect()
CsrfProtect(app)
csrf.init_app(app)

db = SQLAlchemy(app)

db.create_all()

from app.views.base_views import view

app.register_blueprint(view)

