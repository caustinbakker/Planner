#!/usr/bin/env python3
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
    g.db.connect()


@app.after_request
def after_request(response):
    """Close database connection """
    g.db.close()
    return response


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
    try:
        planning = models.Planning.get(models.Planning.planning_name ==
                                       planning_name)
    except DoesNotExist:
        flash('Planning does not exist', 'error')
        return redirect(url_for('create_planning'))
    return render_template("planning.html",
                           planning_name=planning.planning_name,
                           created_at=planning.Created_at.date(),
                           status=planning.status,
                           days_left=((planning.end_date.date() -
                                       date.today()).days),
                           dates=date_range(planning.start_date,
                                            planning.end_date),
                           procent=int((100 / len((date_range(planning.start_date, planning.end_date))))) * ((date.today() - planning.start_date.date()).days)
                           #procent = ((date.today() - planning.start_date.date()).days)
                           #procent = (planning.start_date.date() - date.today()).days
                           )


@app.route('/remove_planning')
def remove_planning():
    return render_template('remove_planning.html')


def date_range(begin_date, end_date):
    dates = []
    while begin_date != end_date:
        dates.append(str(begin_date.date()))
        begin_date += timedelta(days=1)
    return dates


if __name__ == '__main__':
    models.initialize()


app.run(debug=DEBUG, port=PORT, host=HOST)
