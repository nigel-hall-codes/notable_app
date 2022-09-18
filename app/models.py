from peewee import *

db = SqliteDatabase("app/models.db")

class Physicians(Model):
    physicianId = AutoField()
    firstName = CharField()
    lastName = CharField()

    class Meta:
        database = db


class Appointments(Model):
    appointmentId = AutoField()
    lastName = CharField()
    firstName = CharField()
    dt = DateTimeField()
    kind = CharField()
    physicianId = IntegerField()

    class Meta:
        database = db

db.connect()
db.create_tables([Physicians, Appointments])