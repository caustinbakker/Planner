#! \Venv\Scriptsactivate_this.py

from flask import Flask, g, render_template, redirect, url_for, flash
from peewee import *
from datetime import timedelta, date


import forms
import models

DEBUG = True
PORT = 5000
HOST = '127.0.0.1'


app = Flask(__name__)
app.secret_key = '124312415634f35fdf89hg489hjf9092j23jjf9928fisd02d0k11j90j'


@app.before_request
def before_request():
    """Connect database connect"""
    g.db = models.db
    try:
        g.db.connect()
    except OperationalError:
        g.db.close()


@app.after_request
def after_request(response):
    """Close database connection """
    g.db.close()
    return response


@app.route('/planning/<planning_name>/addtask', methods=('GET', 'POST'))
def addtask(planning_name):
    form = forms.AddTask()
    if form.validate_on_submit():
        models.Task.create_task(
            planning=models.Planning.get(models.Planning.planning_name ==
                                         planning_name).id,
            task=form.name.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            desc=form.desc.data
        )
        return redirect(url_for('planning', planning_name=planning_name))
    return render_template('addtask.html', form=form)


@app.route('/create_planning', methods=('GET', 'POST'))
def create_planning():
    form = forms.AddPlanning()
    if form.validate_on_submit():
        try:
            models.Planning.create_planning(
                planning_name=form.planning_name.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data
            )
        except ValueError:
            flash('planning exists', 'error')
        return redirect(url_for('planning',
                                planning_name=form.planning_name.data))
    return render_template('create_planning.html', form=form)


@app.route('/planning/<planning_name>')
def planning(planning_name):
    form = forms.AddPlanning()
    try:
        planning = models.Planning.get(models.Planning.planning_name ==
                                       planning_name)
    except DoesNotExist:
        flash('[error]Planning does not exist', 'error')
        return redirect(url_for('create_planning'))
    return render_template("planning.html",
                           planning_name=planning.planning_name,
                           created_at=planning.Created_at.date(),
                           status=planning.status,
                           days_left=((planning.end_date.date() -
                                       date.today()).days),
                           dates=date_range(planning.start_date,
                                            planning.end_date),
                           procent = calculate_procent(planning.start_date,
                                                       planning.end_date),
                           form=form,
                           planning=models.Planning.get((models.Planning.
                                                         planning_name) ==
                                                        planning_name)
                           )


@app.route('/remove_planning')
def remove_planning():
    return render_template('remove_planning.html')


def date_range(begin_date, end_date):
    dates = {}

    try:
        new_month = None
        while begin_date != end_date:
            dates.update({begin_date.__format__('%d-%m-%Y'):
                         {'day': begin_date.__format__('%d'),
                          'year': begin_date.__format__('%Y')}})
            if new_month != begin_date.month:
                new_month = begin_date.month
                dates[begin_date.__format__('%d-%m-%Y')].update(
                    {'month': begin_date.__format__('%B')})
            begin_date += timedelta(days=1)
    except OverflowError:
        flash('Dates are not correct', 'failed')
        return redirect(url_for('create_planning'))
    return dates


def calculate_procent(start_date, end_date):
    procent = int((100 / len(date_range(start_date,
                                        end_date))) *
                  (date.today() - start_date.date()).days)
    if 100 <= procent:
        return 100
    else:
        return procent

if __name__ == '__main__':
    models.initialize()


app.run(debug=DEBUG, port=PORT, host=HOST)
