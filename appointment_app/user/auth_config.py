from flask_login import LoginManager, UserMixin


login_manager = LoginManager()


class Client(UserMixin):
    ''' Client login configuration '''
    def __init__(self, client_id, username, password, email, avatar, phone):
        ''' Constructor with all parameters for a user '''
        self.client_id = client_id
        self.username = username
        self.password = password
        self.email = email
        self.avatar = avatar
        self.phone = phone

    def get_id(self):
        ''' Gets the ID of the user in session'''
        return self.client_id


class Professional(UserMixin):
    ''' Professional login configuration '''
    def __init__(self, professional_id, username, password, email, avatar,
                 phone, pay_rate, speciality):
        self.professional_id = professional_id
        self.username = username
        self.password = password
        self.email = email
        self.avatar = avatar
        self.phone = phone
        self.pay_rate = pay_rate
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
