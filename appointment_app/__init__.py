''' Gets a flask app instance '''
from flask import Flask, render_template
from appointment_app.config import ConfigDev
from appointment_app.main.routes import main
from appointment_app.administration.routes import administration
from appointment_app.appointment.routes import appointment
from appointment_app.user.routes import user
from appointment_app.report.routes import report
from appointment_app.user.auth_config import login_manager
from appointment_app.api.routes import api_blueprint

def create_app(config=ConfigDev):
    ''' Creates an instance of our application with a configuration '''
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(main)
    app.register_blueprint(administration)
    app.register_blueprint(appointment)
    app.register_blueprint(user)
    app.register_blueprint(report)
    app.register_blueprint(api_blueprint)
    
    login_manager.init_app(app)
    
    @app.errorhandler(404)
    def not_found(e):
        return render_template('not-found.html')
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('internal-server-error.html')
    
    return app
