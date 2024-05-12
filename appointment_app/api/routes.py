"""api for application"""
from flask import Blueprint, request, abort, render_template
from flask_restful import Api, Resource
from appointment_app.qdb.database import db
from oracledb import Date

api_blueprint = Blueprint("api", __name__, template_folder="templates", static_folder="static", static_url_path="/static/api")
api = Api(api_blueprint)

@api_blueprint.route("/api-docs")
def api_docs():
    ''' Renders the API documentation'''
    return render_template("api-docs.html")

class Appointments(Resource):
    '''resources for all appointments'''
    def get(self):
        '''get a list of appointments'''
        appts = db.get_appointments(cond=None)
        appts_dict_list = []
        for appt in appts:
            appts_dict_list.append({
                'appointment_id': appt[0],
                'status': appt[1],
                'date': str(appt[2]),
                'slot': appt[3],
                'venue': appt[4],
                'client_id': appt[5],
                'profession_id': appt[6],
                'service_id': appt[7],
            })
        return appts_dict_list, 200
    
    def post(self):
        '''post a new appointment'''
        # get data
        data = request.json
        
        # if the request is empty
        if not data:
            abort(400, "Missing data")
        
        # check all fields to make an appointments object are there
        required_fields = ['status', 'date_appointment', 'slot', 'venue', 'client_id', 'professional_id', 'service_id']
        for field in required_fields:
            if field not in data:
                abort(400, f"Missing field: {field}")
        
        # check if client exists
        client = db.get_user(f"WHERE user_id = {data['client_id']}")
        if not client:
            abort(400, "Client ID not found")
            
        # check if professional exists
        prof = db.get_user(f"WHERE user_id = {data['professional_id']}")
        if not prof:
            abort(400, "Professional ID not found")
            
        # check if service exists
        service = db.get_service(f"WHERE service_id = {data['service_id']}")
        if not service:
            abort(400, "Service not found")
        
        # make an appointment model
        db.add_appointment(status=data['status'],
                           date_appointment=Date.fromisoformat(data['date_appointment'].split(' ')[0]),
                           slot=data['slot'],
                           venue=data['venue'],
                           client_id=data['client_id'],
                           professional_id=data['professional_id'],
                           service_id=data['service_id'])
        return '', 200
        

class Appointment(Resource):
    '''resource for single appointment'''
    def get(self, appointment_id):
        '''get a single appointment'''
        
        # check if the appointment exists
        if not self.__exists(appointment_id):
            abort(400, "Appointment not found")
        
        # get the appointment
        appt = db.get_appointment(f"WHERE appointment_id={appointment_id}")
        appts_dict_list = {
            'appointment_id': appt[0],
            'status': appt[1],
            'date': str(appt[2]),
            'slot': appt[3],
            'venue': appt[4],
            'client_id': appt[5],
            'professional_id': appt[6],
            'service_id': appt[7],
        }
        return appts_dict_list, 200
    
    def delete(self, appointment_id):
        '''Delete a appointment'''
        if not self.__exists(appointment_id):
            abort(400, "Appointment not found")
        db.delete_appointment(appointment_id)
        return '', 200

    def patch(self, appointment_id):
        '''Update a appointment in the database'''
        if not self.__exists(appointment_id):
            abort(400, message='Appointment does not exist')
        data = request.json
        # check all fields to make an appointments object are there
        required_fields = ['status', 'date_appointment', 'slot', 'venue', 'service_id', 'number_of_services']
        for field in required_fields:
            if field not in data:
                abort(400, f"Missing field: {field}", )
        service = db.get_service(f"WHERE service_id = {data['service_id']}")
        if not service:
            abort(400, "Service not found")
        db.update_appointment(  appointment_id, 
                                date_appointment=Date.fromisoformat(data['date_appointment'].split(' ')[0]),
                                slot=data['slot'], 
                                venue=data['venue'], 
                                service_id=data['service_id'])
        return '', 200
    
    def __exists(self, appointment_id):
        '''Check if the appointment exists in the database'''
        appt = db.get_appointment(f"WHERE appointment_id = {appointment_id}")
        return appt
    
    
api.add_resource(Appointments, "/api/appointments")
api.add_resource(Appointment , "/api/appointments/<int:appointment_id>")