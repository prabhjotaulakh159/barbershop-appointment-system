from flask_login import LoginManager, UserMixin


login_manager = LoginManager()


class User(UserMixin):
    ''' Base class representing a user '''

    def __init__(self, username, password, email, avatar, phone):
        self.username = username
        self.password = password
        self.email = email
        self.avatar = avatar
        self.phone = phone

class Client(User):
    ''' Class representing a client '''
    def __init__(self, client_id, username, password, email, avatar, phone):
        super().__init__(username, password, email, avatar, phone)
        self.client_id = client_id
    
    def get_id(self):
        ''' Gets the ID of the user in session'''
        return self.client_id

class Professional(User):
    ''' Professional login configuration '''

    def __init__(self, professional_id, username, password, email, avatar,
                 phone, pay_rate, speciality):
        super().__init__(username,password,email,avatar,phone)
        self.professional_id = professional_id
        self.payrate = pay_rate
        self.specialty = speciality


login_manager = LoginManager()


@login_manager.user_loader
def load_client(client_id, username, password, email, avatar, phone):
    ''' Loads the client from the session '''
    return Client(client_id, username, password, email, avatar, phone)


@login_manager.user_loader
def load_professional(professional_id, username, password, email, avatar,
                      phone, pay_rate, speciality):
    ''' Loads the professional from the session '''
    return Professional(professional_id, username, password, email, avatar,
                        phone, pay_rate, speciality)


@login_manager.unauthorized_handler
def unauthorized():
    ''' Redirects to a login page if user accesses an unauthorized page '''
    pass
