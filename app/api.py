from app.models import Physicians, Appointments
import pandas as pd


class API:
    def get_physicians(self):

        p = Physicians.select().dicts()
        df = pd.DataFrame(list(p))
        df['Name'] = df['lastName'] + ", " + df['firstName']
        df['id'] = df['physicianId']
        df = df[['id', "Name"]]
        df.columns = ["id", 'Name']

        return df


    def get_physician_appointments_for_day(self, physicianId, date):

        a = Appointments.select().where(Appointments.physicianId == physicianId).dicts()
        df = pd.DataFrame(list(a))

        df['date'] = df['dt'].apply(lambda x: x.strftime("%m-%d-%Y"))
        df = df[df['date'] == date]
        df['Name'] = df['lastName'] + ", " + df['firstName']
        df['Time'] = df['dt'].apply(lambda x: x.strftime("%H:%M%p"))

        df['#'] = df['appointmentId']

        return df[['#', "Name", "Time", "kind"]]


# a = API()
# print(a.get_physician_appointments_for_day(1, "09-19-2022"))
# print(a.get_physicians())

