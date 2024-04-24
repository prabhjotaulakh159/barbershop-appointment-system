from flask import redirect, url_for
from flask_login import LoginManager, UserMixin
from appointment_app.qdb.database import db

login_manager = LoginManager()



class User(UserMixin):
    ''' Base class representing a user '''
    def __init__(self, user_id, is_enabled, access_level, user_type, user_name, pass_word, email, avatar, phone, address, age, pay_rate, specialty):
        self.user_id = user_id
        self.is_enabled = is_enabled
        self.access_level = access_level
        self.user_type = user_type
        self.user_name = user_name
        self.pass_word = pass_word
        self.email = email
        self.avatar = avatar
        self.phone = phone
        self.address = address
        self.age = age
        self.pay_rate = pay_rate
        self.specialty = specialty
        
    def get_id(self):
        return self.user_name
    
    def is_active(self):
        return self.is_enabled


@login_manager.user_loader
def load_user(user_id):
    user = db.get_user(user_id)
    return User(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8], user[9], user[10], user[11], user[12])

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('user.login'))
