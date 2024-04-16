from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class AddjobForm(FlaskForm):
    job = StringField('Job Title', validators=[DataRequired()])
    team_leader = IntegerField('Team Leader (id)', validators=[DataRequired()])
    work_size = IntegerField('Work Size (hours)', validators=[DataRequired()])
    collaborators = StringField('Collaborators (ids)', validators=[DataRequired()])
    category = IntegerField('Hazard Category', validators=[DataRequired()])
    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Add')