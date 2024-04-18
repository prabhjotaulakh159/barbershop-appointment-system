from flask import Flask
from project.config import ConfigDev
from flask_login import LoginManager


def create_app(config=ConfigDev):
    app = Flask(__name__)
    app.config.from_object(config)

    from project.main.routes import main
    from project.administration.routes import administration
    from project.appointment.routes import appointment
    from project.user.routes import user
    from project.report.routes import report

    app.register_blueprint(main)
    app.register_blueprint(administration)
    app.register_blueprint(appointment)
    app.register_blueprint(user)
    app.register_blueprint(report)
    
    return app
