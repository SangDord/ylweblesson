from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired


class GaleryForm(FlaskForm):
    picture = FileField('Добавить картинку', validators=[DataRequired()])
    submit = SubmitField('Отправить', validators=[DataRequired()])