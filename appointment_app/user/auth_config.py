from flask_login import LoginManager, UserMixin

login_manager = LoginManager()

class User(UserMixin):
    ''' Extends UserMixing for flask login '''
    
    def __init__(self):
        ''' Constructor '''
        pass

    def get_id(self):
        ''' Gets the ID of the user in session'''
        pass

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    ''' Loads the user from session '''
    pass

@login_manager.unauthorized_handler
def unauthorized():
    ''' Redirects to some page if not authorized '''
    pass
