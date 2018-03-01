from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms import DateField, StringField


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
    task_name = StringField('task_name',
                            validators=[DataRequired()])


def planning_exists(form, field):
    if Planning.select().where(Planning.planning_name == field.data).exists():
        raise ValidationError('User with that name already exists.')
