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


class Task(Model):
    planning = ForeignKeyField(Planning, backref='Task')
    task = CharField()
    task_num = IntegerField(unique=True)
    start_date = DateTimeField()
    end_date = DateTimeField()
    desc = CharField()

    class Meta(object):
        database = db

    @classmethod
    def create_task(cls, planning, task, start_date, end_date, desc):
        cls.create(
            planning=planning,
            task=task,
            start_date=start_date,
            end_date=end_date,
            desc=desc
        )


class Date(Model):
    task = ForeignKeyField(Task, backref='Date')
    date = DateTimeField(default=date.today)
    status = IntegerField(default=1)

    class Meta(object):
        database = db

    @classmethod
    def create_date(cls, task):
        cls.create(
            task=task
        )


def initialize():
    db.connect()
    db.create_tables([Planning, Task, Date], safe=True)
    db.close()
