''' Contains config for different environnements '''
import dotenv as env
import os

env.load_dotenv()

class ConfigDev:
    ''' Condifuration for dev env'''
    SECRET_KEY = '413de6338d72b9071370af8534c6213b' #os.environ.get('SECRET_KEY')
    DEBUG = True
    APP_ENV = "develop"


class ConfigProd:
    ''' Condifuration for prod env'''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    APP_ENV = "production"