import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from FirebaseConfig import real_time_db_url, credential_path

cred = credentials.Certificate(credential_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': real_time_db_url
})

db_ref = db


def update_weather(data):
    global db
    weather_db = db.reference('weather/').get()
    weather_db_keys = list(weather_db.keys())
    db.reference('weather/{0}'.format(weather_db_keys[0])).update(data)
