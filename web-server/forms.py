from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Логин', [Length(min=2, max=20), DataRequired()])
    password = PasswordField('Пароль', [Length(min=6, max=30), DataRequired()])
    # remember = BooleanField('Запомнить меня', default=False)
    submit = SubmitField('Войти')
