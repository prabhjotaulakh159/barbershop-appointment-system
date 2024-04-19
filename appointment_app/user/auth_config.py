from flask_login import LoginManager, UserMixin
from flask_login import UserMixin
from appointment_app.qdb.database import db

login_manager = LoginManager()

class User(UserMixin):
    ''' Base class representing a user '''
    def __init__(self, username, password, email, avatar, phone):
        self.username = username
        self.password = password
        self.email = email
        self.avatar = avatar
        self.phone = phone

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


class Client(User):
    ''' Class representing a client '''
    def __init__(self, username):
        client = db.get_client(username)
        super().__init__(client[1], client[2], client[3], client[4], client[5])
        
class Professional(User):
    ''' Class representing a professional '''
    def __init__(self, username):
        professional = db.get_professional(username)
        super().__init__(professional[1], professional[2], professional[3], professional[4], professional[5])
        self.payrate = professional[6]  
        self.specialty = professional[7]

    def __str__(self):
        return f"{super().__str__()} {self.payrate} {self.specialty}"


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    ''' Loads the user from session '''
    pass


@login_manager.unauthorized_handler
def unauthorized():
    ''' Redirects to some page if not authorized '''
    pass
