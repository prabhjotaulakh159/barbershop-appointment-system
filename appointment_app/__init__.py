from flask import Flask
from appointment_app.config import ConfigDev

def create_app(config=ConfigDev):
    ''' Creates an instance of our application with a configuration '''
    app = Flask(__name__)
    app.config.from_object(config)

    from appointment_app.main.routes import main
    from appointment_app.administration.routes import administration
    from appointment_app.appointment.routes import appointment
    from appointment_app.user.routes import user
    from appointment_app.report.routes import report
    from appointment_app.user.auth_config import login_manager

    app.register_blueprint(main)
    app.register_blueprint(administration)
    app.register_blueprint(appointment)
    app.register_blueprint(user)
    app.register_blueprint(report)
    
    login_manager.init_app(app)
    
    return app
