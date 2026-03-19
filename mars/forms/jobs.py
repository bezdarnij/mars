from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField("Название", validators=[DataRequired()])
    work_size = IntegerField("Продолжительность работы", validators=[DataRequired()])
    collaborators = StringField("Коллеги", validators=[DataRequired()])
    team_leader = IntegerField("ID руководителя", validators=[DataRequired()])
    is_finished = BooleanField("Завершена ли работа?")
    submit = SubmitField("Создать")
