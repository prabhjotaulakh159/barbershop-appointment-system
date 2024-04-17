from flask import Flask
from project.config import ConfigDev
from flask_login import LoginManager


def create_app(config = ConfigDev ):
    app = Flask(__name__)
    app.config.from_object(config)
    
    from project.main.routes import main


    app.register_blueprint(main)
    
    return app

