'''import flask and its methods'''
from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_login import login_required, current_user
from appointment_app.appointment.appointment import Appointment
from appointment_app.qdb.database import db
from appointment_app.appointment.forms import AppointmentForm, AppointmentAdminForm
from appointment_app.appointment.utility import time_slots, venues
import pdb
appointment = Blueprint('appointment', __name__, template_folder="templates")


@appointment.route('/all-appointments')
def all_appointments():
    appointments = db.get_appointments()
    return render_template("all-appointments.html", appointments=appointments)


@appointment.route('/all-appointments/<int:appointment_id>')
@login_required
def appointment_view(appointment_id):
    appt = db.get_appointment(f"appointment_id = {appointment_id}")
    client_name = db.get_user(f"WHERE user_id = {appt[5]}")
    professional_name = db.get_user(f"WHERE user_id = {appt[6]}")
    service_name = db.get_service(f"WHERE service_id = {appt[7]}")[0]

    names = []
    names.append(client_name[4])
    names.append(professional_name[4])
    names.append(service_name[0])

    return render_template("specific-appointment.html", appointment=appt, names=names)


@appointment.route('/my-appointments')
@login_required
def my_appointments():
    appointments = db.get_appointments(
        f"WHERE client_id = {current_user.user_id} OR professional_id = {current_user.user_id}")
    names = []    
    reports = []    
    for appt in appointments:    
        client_name = db.get_user(f"WHERE user_id = {appt[5]}")
        professional_name = db.get_user(f"WHERE user_id = {appt[6]}")
        service_name = db.get_service(f"WHERE service_id = {appt[7]}")[0]
        names.append((client_name[4], professional_name[4],service_name[0]))
        reports.append(db.get_report(appt[0]))
    return render_template("my-appointments.html", appointments=appointments, names=names, reports=reports)


@appointment.route("/add-appointment", methods=["GET", "POST"])
@login_required
def add_appointment():
    if current_user.user_type == 'Professional':
        return redirect(url_for('main.home'))
    # import pdb
    form = AppointmentForm()

    services = db.get_services()
    services_list = []
    # pdb.set_trace()
    for service in services:
        services_list.append((service[1], service[1]))

    professionals = db.get_users(f"WHERE user_type = 'Professional'")
    professionals_list = []
    for professional in professionals:
        professionals_list.append((professional[4], professional[4]))

    form.prof_name.choices = professionals_list
    form.service.choices = services_list
    form.slot.choices = time_slots
    form.venue.choices = venues
    if form.validate_on_submit():

        status = 1
        client_id = current_user.user_id
        prof_id = db.get_user(f"WHERE user_name = '{form.prof_name.data}'")[0]
        service_id = db.get_service(f"WHERE service_name = '{form.service.data}'")[0]
        db.add_appointment(status, form.date_appointment.data,
                           form.slot.data, form.venue.data, client_id, prof_id, service_id)
        flash('Appointment is created!')

    return render_template("add-appointment.html", form=form)


@appointment.route("/update-appointment/<int:appointment_id>", methods=['GET', 'POST'])
@login_required
def update_appointment(appointment_id):
    if current_user.user_type == 'Professional':
        return redirect(url_for('main.home'))
    appointment = db.get_appointment(f"appointment_id = {appointment_id}")
    if (current_user.user_id != appointment[5] and current_user.user_id != appointment[6]) and current_user.access_level < 2:
        return redirect(url_for('main.home'))

    if (current_user.access_level >= 2):
        form = AppointmentAdminForm()
    else:
        form = AppointmentForm()

    if request.method == 'GET':
        form.date_appointment.data = appointment[2]
        form.slot.data = appointment[3]
        form.venue.data = appointment[4]
        form.service.data = db.get_service(f"WHERE service_id = {appointment[7]}")[1]
        services = db.get_services()
        services_list = []

        for service in services:
            services_list.append((service[1], service[1]))

        professionals = db.get_users(f"WHERE user_type = 'Professional'")
        professionals_list = []
        for professional in professionals:
            professionals_list.append((professional[4], professional[4]))


        form.prof_name.choices = professionals_list
        form.service.choices = services_list
        form.slot.choices = time_slots
        form.venue.choices = venues

        if (current_user.access_level >= 2):
            members = db.get_users(f"WHERE user_type = 'Member'")
            members_list = []
            for member in members:
                members_list.append((member[4], member[4]))
                form.member_name.choices = members_list

    else:
        service_id = db.get_service(f"WHERE service_name = '{form.service.data}'")[0]
        if (current_user.access_level >= 2):
            client_id = db.get_user(f"WHERE user_name = '{form.member_name.data}'")[0]
            prof_id = db.get_user(f"WHERE user_name = '{form.prof_name.data}'")[0]

            db.update_appointment(appointment_id=appointment[0], date_appointment=form.date_appointment.data,
                                        slot=form.slot.data, venue=form.venue.data, client_id=client_id, professional_id=prof_id, service_id=service_id)
        else:
            db.update_appointment(appointment_id=appointment[0], date_appointment=form.date_appointment.data,
                                  slot=form.slot.data, venue=form.venue.data, service_id=service_id)
        flash("You have successfully updated the appointment!", "success")
        return redirect(url_for('main.home'))
    return render_template('update-appointment.html', current_user=current_user, form=form)


@appointment.route('/admin-appointments', methods=["GET", "POST"])
@login_required
def admin_appointments():
    if current_user.access_level < 2:
        return redirect(url_for('main.home'))

    form = AppointmentAdminForm()

    members = db.get_users(f"WHERE user_type = 'Member'")
    members_list = []
    for member in members:
        members_list.append((member[4], member[4]))

    services = db.get_services()
    services_list = []
    for service in services:
        services_list.append((service[1], service[1]))

    professionals = db.get_users(f"WHERE user_type = 'Professional'")
    professionals_list = []
    for professional in professionals:
        professionals_list.append((professional[4], professional[4]))

    form.member_name.choices = members_list
    form.prof_name.choices = professionals_list
    form.service.choices = services_list
    form.slot.choices = time_slots
    form.venue.choices = venues

    if form.validate_on_submit():

        status = 1
        client_id = db.get_user(f"WHERE user_name = '{form.member_name.data}'")[0]
        prof_id = db.get_user(f"WHERE user_name = '{form.prof_name.data}'")[0]
        service_id = db.get_service(f"WHERE service_name = '{form.service.data}'")[0]
        db.add_appointment(status, form.date_appointment.data,
                           form.slot.data, form.venue.data, client_id, prof_id, service_id)
        flash('Appointment is created!')

    appointments = db.get_appointments()
    names = []

    for apt in appointments:
        client_name = db.get_user(f"WHERE user_id= {apt[5]}")
        professional_name = db.get_user(f"WHERE user_id = {apt[6]}")
        service_name = db.get_service(f"WHERE service_id = {apt[7]}")

        names.append((client_name[4], professional_name[4], service_name[1]))

    return render_template("admin-appointments.html", form=form, appointments=appointments, names=names)


@appointment.route('/delete-appointment/<int:appointment_id>')
@login_required
def delete_appointment(appointment_id):
    if current_user.access_level < 2:
        return redirect(url_for('main.home'))
    
    db.delete_appointment(appointment_id)
    flash("Appointment is deleted!")
    return redirect(url_for('appointment.admin_appointments'))
    
