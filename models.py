from peewee import *
from datetime import date

db = SqliteDatabase('planning.db')


class Planning(Model):
    planning_name = CharField(unique=True)
    start_date = DateTimeField()
    end_date = DateTimeField()
    Created_at = DateTimeField(default=date.today)
    status = IntegerField(default=0)

    class Meta(object):
        database = db

    def get_dates(self):
        return Date.select().where(Date.planning == self)

    @classmethod
    def create_planning(cls, planning_name, start_date, end_date):
        try:
            cls.create(
                planning_name=planning_name,
                start_date=start_date,
                end_date=end_date
            )
        except IntegrityError:
            raise ValueError("Planning already exists")


class Date(Model):
    planning = ForeignKeyField(Planning, backref='Date')
    date = DateTimeField()
    task = CharField()
    status = IntegerField(default=0)

    class Meta(object):
        database = db


def initialize():
    db.connect()
    db.create_tables([Planning, Date], safe=True)
    db.close()
