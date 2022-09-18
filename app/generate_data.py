import faker
from models import Physicians, Appointments
import datetime
import random

fake = faker.Faker()

def create_physicians():
    p_data = [
        {"lastName": "Hibbert", "firstName": "Julius"},
        {"lastName": "Krieger", "firstName": "Algernop"},
        {"lastName": "Riviera", "firstName": "Nick"}
    ]

    Physicians.insert_many(p_data).execute()


def create_appointments():

    kinds = ["Follow up", "New Patient"]

    for phys_id in range(1, 4):

        appointment_time = datetime.datetime(day=18, month=9, year=2022, hour=9)

        for x in range(0, 100):

            lastName = fake.last_name()
            firstName = fake.first_name()

            dt = appointment_time
            kind = random.choice(kinds)

            print(f"Creating {lastName, firstName} {dt}, {kind}, {phys_id}")
            Appointments.create(lastName=lastName, firstName=firstName, dt=dt, kind=kind, physicianId=phys_id)



            appointment_time += datetime.timedelta(hours=1)

            if appointment_time.hour > 17:
                appointment_time = datetime.datetime(day=(appointment_time.day + 1),
                                                     hour=9, year=2022, month=9)

def delete_physicians():
    q = Physicians.delete()
    q.execute()










