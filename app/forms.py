from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField
from wtforms import ValidationError, validators

from app.controllers.user_controller import get_user

FieldIsRequiredMessage = 'Поле обязательно'
LoginAlreadyUseMessage = 'Пользователь с таким логином уже существует'


def validate_name(Form, field):
    check = get_user(field.data)
    if check is not None:
        raise ValidationError(LoginAlreadyUseMessage)


class LoginForm(FlaskForm):
    login = StringField('login', [validators.length(min=1, max=25, message=FieldIsRequiredMessage)])
    password = PasswordField('password', [validators.length(min=1, message=FieldIsRequiredMessage)])


class RegisterForm(FlaskForm):
    login = StringField('login', [validators.length(min=1, message=FieldIsRequiredMessage), validate_name])
    password = PasswordField('password', [validators.length(min=1, message=FieldIsRequiredMessage)])
    fio = StringField('fio', [validators.length(min=1, message=FieldIsRequiredMessage)])
    confirm = PasswordField('Repeat Password',[validators.EqualTo('password')])
