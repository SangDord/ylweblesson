from wtforms import EmailField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class AdddepartmentForm(FlaskForm):
    title = StringField('Department Title', validators=[DataRequired()])
    chief = IntegerField('Chief (id)', validators=[DataRequired()])
    members = StringField('Members (ids)', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Add')