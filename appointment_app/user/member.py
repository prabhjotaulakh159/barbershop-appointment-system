'''Module containing the Member Class'''
from flask_login import UserMixin
from appointment_app.qdb.database import db

class Member(UserMixin):
    ''' class representing an member '''
    def __init__(self, username):
        member = db.get_member(username)
        self.username = member[1]
        self.password = member[2]
        self.email = member[3]
        self.avatar = member[4]
        self.phone = member[5]

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
