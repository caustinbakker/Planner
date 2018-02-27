#!/usr/bin/env python3
from flask import Flask, g, render_template, redirect, url_for, request, flash
from peewee import *
import datetime
from datetime import datetime, timedelta


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
            flash('planning exists', succcess)
        return redirect(url_for('planning',
                                planning_name=form.planning_name.data))
    return render_template('create_planning.html', form=form)


@app.route('/planning')
def planning():
    return render_template("planning.html")


@app.route('/remove_planning')
def remove_planning():
    return render_template('remove_planning.html')


def date_range(begin_date, end_date):
    num_date = {}
    daynum = 0
    while begin_date != end_date:
        num_date.update({daynum: str(begin_date)})
        daynum += 1
        begin_date += timedelta(days=1)
    return num_date


if __name__ == '__main__':
    models.initialize()


app.run(debug=DEBUG, port=PORT, host=HOST)
