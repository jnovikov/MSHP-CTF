import os

CSRF_ENABLED = True
DEBUG = os.environ.get('DEBUG', '')
SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
SALT = os.environ.get('SALT', 'SALT')
SQLITE_DB_PATH = os.environ.get('DB_FILE', '/new.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLITE_DB_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = True
if DEBUG != '':
    SQLALCHEMY_ECHO = True
CHECK_USER_ACTIVE = False
