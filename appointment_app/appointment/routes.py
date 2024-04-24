'''import flask and its methods'''
from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from appointment_app.qdb.database import db
from appointment_app.appointment.forms import AppointmentForm

appointment = Blueprint('appointment', __name__, template_folder="templates")


@appointment.route('/all-appointments')
@login_required
def all_appointments():
    appointments = db.get_appointments()
    return render_template("all-appointments.html", appointments=appointments)


@appointment.route("/add-appointment", methods=["GET", "POST"])
@login_required
def add_appointment():
    form = AppointmentForm()

    services = db.get_services_name()
    print(services)
    services_list = []
    for service in services:
        services_list.append((service[0], service[0]))

   
    professionals = db.get_professional_names()
    professionals_list = []
    print(professionals_list)
    for professional in professionals:
        professionals_list.append((professional[0], professional[0]))

    time_slots = [
        ('10-11', '10am - 11am'),
        ('11-12', '11am - 12pm'),
        ('12-1', '12pm - 1pm'),
        ('1-2', '1pm - 2pm'),
        ('2-3', '2pm - 3pm'),
        ('3-4', '3pm - 4pm')
    ]

    venue = [
        ('Venue A', 'Venue A'),
        ('Venue B', 'Venue B'),
        ('Venue C', 'Venue C'),
        ('Venue D', 'Venue D'),
        ('Venue E', 'Venue E'),
    ]

    form.prof_name.choices = professionals_list
    form.service.choices = services_list
    form.slot.choices = time_slots
    form.venue.choices = venue
    if form.validate_on_submit():
        
        status = 1
        client_id = current_user.user_id
        prof_id = db.get_user_id(f"user_name ='{form.prof_name.data}'")[0]
        service_id = db.get_service_id(form.service.data)[0]
        db.add_appointment(status, form.date_appointment.data,
                           form.slot.data, form.venue.data, client_id, prof_id, service_id)
        flash('Appointment is created!')

    return render_template("add-appointment.html", form=form)
