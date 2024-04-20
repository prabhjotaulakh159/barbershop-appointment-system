'''import flask and its methods'''
from flask import Blueprint, render_template, flash
from flask_login import current_user
from appointment_app.qdb.database import Database
from appointment_app.appointment.forms import AppointmentForm
from appointment_app.qdb.database import Database

appointment = Blueprint('appointment', __name__, template_folder="templates",
                        static_folder="static")

db = Database()


@appointment.route("/add_appointment", methods=["GET", "POST"])
def add_appointment():
    form = AppointmentForm()

    services = db.get_services_name()
    services_list = []
    for service in services:
        services_list.append((service[0], service[0]))

    professionals = db.get_professional_names()
    professionals_list = []
    for professional in professionals:
        professionals_list.append((professional[0], professional[0]))

    form.prof_name.choices = professionals_list
    form.service.choices = services_list

    if form.validate_on_submit():
        #no validation yet for time slot & professional being taken. Don't know how to do it
        
        status = 1
        client_id = 1  # to be replaced with current_user.client_id once login works
        prof_id = db.get_professional_id(form.prof_name.data)[0]
        service_id = db.get_service_id(form.service.data)[0]
        db.add_appointment(status, form.date_appointment.data,
                           form.slot.data, form.venue.data, client_id, prof_id, service_id)
        flash('Appointment is created!')
    
    return render_template("appointment.html", form=form)
