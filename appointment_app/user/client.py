'''Module containing the client Class'''
from flask_login import UserMixin
from appointment_app.qdb.database import db

class Client(UserMixin):
    ''' class representing a client '''
    def __init__(self, username):
        client = db.get_client(username)
        self.username = client[1]
        self.password = client[2]
        self.email = client[3]
        self.avatar = client[4]
        self.phone = client[5]

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return f"{self.username} {self.email} {self.phone}"
