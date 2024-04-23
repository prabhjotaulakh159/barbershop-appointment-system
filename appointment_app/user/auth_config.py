from flask_login import LoginManager, UserMixin


login_manager = LoginManager()


class User(UserMixin):
    ''' Base class representing a user '''
    def __init__(self, user_id, is_active, access_level, user_type, user_name, 
                 pass_word, email, avatar, phone, address, age, pay_rate, specialty):
        self.user_id = user_id
        self.is_active = is_active
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


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id, is_active, access_level, user_type, user_name, 
                pass_word, email, avatar, phone, address, age, pay_rate, specialty):
    ''' Loads the client from the session '''
    return User(user_id, is_active, access_level, user_type, user_name, pass_word, email, avatar,
                phone, address, age, pay_rate, specialty)

@login_manager.unauthorized_handler
def unauthorized():
    ''' Redirects to a login page if user accesses an unauthorized page '''
    pass
