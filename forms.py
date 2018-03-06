from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms import DateField, StringField, RadioField
import datetime

from models import Planning


class AddPlanning(FlaskForm):
    """Add planning to database"""
    planning_name = StringField('Planning name',
                                validators=[DataRequired()])
    start_date = DateField('begin date DD/MM/YY',
                           format="%d/%m/%Y",
                           validators=[DataRequired()])
    end_date = DateField('end date DD/MM/YY',
                         format="%d/%m/%Y",
                         validators=[DataRequired()])


class AddTask(FlaskForm):
    """Add Task to your planning"""
    months = []
    for month in range(1, 13):
        months.append((month, datetime.date(2008, month, 1).strftime('%B')))
    test1 = RadioField(choices=(months), id='date_select')


def planning_exists(form, field):
    if Planning.select().where(Planning.planning_name == field.data).exists():
        raise ValidationError('User with that name already exists.')
