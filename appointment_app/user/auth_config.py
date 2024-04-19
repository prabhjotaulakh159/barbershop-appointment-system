from flask_login import LoginManager, UserMixin
from flask_login import UserMixin
from appointment_app.qdb.database import db

login_manager = LoginManager()

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


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    ''' Loads the user from session '''
    pass


@login_manager.unauthorized_handler
def unauthorized():
    ''' Redirects to some page if not authorized '''
    pass
