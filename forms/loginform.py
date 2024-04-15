from wtforms import EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class LoginFrom(FlaskForm):
    email = EmailField('Email', validators=[DataRequired])
    password = PasswordField('Password', validators=[DataRequired])
    remember_be = BooleanField('Remember me', validators=[DataRequired])
    submit = SubmitField('Log in')