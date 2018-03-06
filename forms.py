from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms import DateField, StringField, RadioField

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
    years = [('2017', '2017'), ('2018', '2018'), ('2019', '2019'),
             ('2020', '2020'), ('2021', '2021'), ('2022', '2022')]
    months = [('January', 'January'), ('February', 'February'),
              ('March', 'March'), ('April', 'April'), ('May', 'May'),
              ('June', 'June'), ('July', 'July'), ('August', 'August'),
              ('September', 'September'), ('October', 'October'),
              ('November', 'November'), ('December', 'December')]
    days = []
    for day in range(1, 32):
        days.append((str(day), str(day)))
    year = RadioField('year', choices=(years), id='date_year')
    month = RadioField('month', choices=(months), id='date_month')
    day = RadioField('day', choices=(days), id='date_day')


def planning_exists(form, field):
    if Planning.select().where(Planning.planning_name == field.data).exists():
        raise ValidationError('User with that name already exists.')
