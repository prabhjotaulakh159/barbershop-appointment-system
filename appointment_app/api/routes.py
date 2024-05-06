"""api for application"""
from flask import Blueprint, request
from flask_restful import Api, Resource
from appointment_app.qdb.database import db

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)


class Appointments(Resource):
    '''resources for appointments'''
    def get(self):
        '''get a list of appointments'''
        appts = db.get_appointments(cond=None)
        return appts
    
    def post(self):
        '''post a new appointment'''
        data = request.json()
        status = data['status']
        date_appointment = data['date_appointment']
        slot = data['slot']
        venue = data['venue']
        client_id = data['client_id']
        professional_id = data['professional_id']
        service_id = data['service_id']
        db.add_appointment(status=status,
                           date_appointment=date_appointment,
                           slot=slot,
                           venue=venue,
                           client_id=client_id,
                           professional_id=professional_id,
                           service_id=service_id)