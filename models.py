from flask_login import UserMixin
from peewee import *
import datetime

db = SqliteDatabase('planning.db')


class Planning(Model):
    planning_name = CharField(unique=True)
    start_date = DateTimeField()
    end_date = DateTimeField()
    Created_at = DateTimeField(default=datetime.datetime.now)
    status = IntegerField(default=0)

    class Meta:
        database = db

    @classmethod
    def create_planning(cls, planning_name, start_date, end_date):
        try:
            cls.create(
                planning_name=planning_name,
                start_date=start_date,
                end_date=end_date,
                )
        except IntegrityError:
            raise ValueError("Planning already exists")


def initialize():
    db.connect()
    db.create_tables([Planning], safe=True)
    db.close()
