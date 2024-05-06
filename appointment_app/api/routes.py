"""api for application"""
from flask import Blueprint, request, abort
from flask_restful import Api, Resource
from appointment_app.qdb.database import db


api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)


class Appointments(Resource):
    '''resources for all appointments'''
    def get(self):
        '''get a list of appointments'''
        appts = db.get_appointments(cond=None)
        return appts
    
    def post(self):
        '''post a new appointment'''
        # get data
        data = request.json
        
        # if the request is empty
        if not data:
            abort(code=400, message="Missing data")
        
        # check all fields to make an appointments object are there
        required_fields = ['status', 'date_appointment', 'slot', 'venue', 'client_id', 'professional_id', 'service_id']
        for field in required_fields:
            if field not in data:
                abort(code=400, message=f"Missing field: {field}")
        
        # check if client exists
        client = db.get_user(f"WHERE client_id = {data['client_id']}")
        if not client:
            abort(code=400, message="Client ID not found")
            
        # check if professional exists
        prof = db.get_user(f"WHERE professional_id = {data['professional_id']}")
        if not prof:
            abort(code=400, message="Professional ID not found")
            
        # check if service exists
        service = db.get_service(f"WHERE service_id = {data['service_id']}")
        if not service:
            abort(code=400, message="Service not found")
        
        # make an appointment model
        db.add_appointment(status=data['status'],
                           date_appointment=data['date_appointment'],
                           slot=data['slot'],
                           venue=data['venue'],
                           client_id=data['client_id'],
                           professional_id=data['professional_id'],
                           service_id=data['service_id'])
        

class Appointment(Resource):
    '''resource for single appointment'''
    def get(self, appointment_id):
        '''get a single appointment'''
        
        # check if the appointment exists
        if not self.__exists(appointment_id):
            abort(code=400, message="Appointment not found")
        
        # get the appointment
        appt = db.get_appointment(f"WHERE appointment_id={appointment_id}")
        return appt
    
    def __exists(self, appointment_id):
        '''Check if the appointment exists in the database'''
        appt = db.get_appointment(f"WHERE appointment_id = {appointment_id}")
        return appt