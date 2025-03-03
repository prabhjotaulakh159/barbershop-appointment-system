'''import flask and its methods'''
from datetime import date
from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_login import login_required, current_user
from appointment_app.qdb.database import db
from appointment_app.appointment.forms import AppointmentForm, AppointmentAdminForm
from appointment_app.appointment.utility import time_slots, venues, appointment_status

appointment = Blueprint('appointment', __name__,
                        static_folder="static",
                        template_folder="templates", static_url_path="/static/appointment")


@appointment.route('/all-appointments')
def all_appointments():
    '''function rendering all appointments'''

    filter_by = request.args.get('filter')
    search = request.args.get('search')
    order_by = request.args.get('order_by')

    if filter_by and search:
        cond = f"WHERE {filter_by} = '{search}'"
    else:
        cond = None

    if order_by:
        if cond:
            cond = cond+f" ORDER BY {order_by}"
        else:
            cond = f"ORDER BY {order_by}"

    appointments = db.get_appointments(cond)
    return render_template("all-appointments.html", appointments=appointments)


@appointment.route('/all-appointments/<int:appointment_id>')
@login_required
def appointment_view(appointment_id):
    '''function rendering specific appointment with appointment_id'''

    cond = f'''WHERE a4.appointment_id = {appointment_id}'''
    appt = db.get_appts_with_joins(cond)[0]

    return render_template("specific-appointment.html",
                           appointment=appt)


@appointment.route('/my-appointments')
@login_required
def my_appointments():
    '''function rendering user's appointments'''
    cond = f'''WHERE u.user_id = {current_user.user_id}
            OR u2.user_id = {current_user.user_id}'''
    order_by = request.args.get('order_by')
    if order_by:
        cond = cond + f" ORDER BY a4.{order_by}"

    appointments = db.get_appts_with_joins(cond)
    return render_template("my-appointments.html", appointments=appointments)


@appointment.route("/add-appointment", methods=["GET", "POST"])
@login_required
def add_appointment():
    '''function that adds an appointments'''
    if current_user.user_type == 'Professional':
        return redirect(url_for('main.home'))

    form = AppointmentForm()
    services = db.get_services()
    services_list = []
    for service in services:
        services_list.append((service[1], service[1]+" "+str(service[3])+"$"))

    professionals = db.get_users("WHERE user_type = 'Professional'")
    professionals_list = []
    for professional in professionals:
        professionals_list.append((professional[4], professional[4]))

    form.prof_name.choices = professionals_list
    form.service.choices = services_list
    form.slot.choices = time_slots
    form.venue.choices = venues
    form.status.choices = appointment_status

    if form.validate_on_submit():

        status = form.status.data
        client_id = current_user.user_id
        prof_id = db.get_user(f"WHERE user_name = '{form.prof_name.data}'")[0]
        service_id = db.get_service(f"WHERE service_name = '{form.service.data}'")[0]
        db.add_appointment(status, form.date_appointment.data,
                           form.slot.data, form.venue.data,
                           client_id, prof_id, service_id)
        db.add_log(f"Created new appointment for client {current_user.user_name}", date.today(), "Appointments", current_user.user_name, current_user.user_id)
        flash('Appointment is created!', "success")

    return render_template("add-appointment.html", form=form)


@appointment.route("/update-appointment/<int:appointment_id>",
                   methods=['GET', 'POST'])
@login_required
def update_appointment(appointment_id):
    '''function updating specific appointments with appointment_id'''
    if current_user.user_type == 'Professional':
        return redirect(url_for('main.home'))
    appt = db.get_appointment(f"WHERE appointment_id = {appointment_id}")
    if current_user.user_id != appt[5] and current_user.access_level < 2:
        return redirect(url_for('main.home'))

    if current_user.access_level >= 2:
        form = AppointmentAdminForm()
    else:
        form = AppointmentForm()

    if request.method == 'GET':
        form.date_appointment.data = appt[2]
        form.slot.data = appt[3]
        form.venue.data = appt[4]
        form.service.data = db.get_service(f"WHERE service_id = {appt[7]}")[1]
        form.status.data = appt[1]

        services = db.get_services()
        services_list = []

        for service in services:
            services_list.append((service[1], service[1]+" "+str(service[3])+"$"))

        professionals = db.get_users("WHERE user_type = 'Professional'")
        professionals_list = []
        for professional in professionals:
            professionals_list.append((professional[4], professional[4]))

        form.prof_name.choices = professionals_list
        form.service.choices = services_list
        form.slot.choices = time_slots
        form.venue.choices = venues
        form.status.choices = appointment_status

        if current_user.access_level >= 2:
            members = db.get_users("WHERE user_type = 'Member'")
            members_list = []
            for member in members:
                members_list.append((member[4], member[4]))
                form.member_name.choices = members_list

    else:

        service_id = db.get_service(f"WHERE service_name = '{form.service.data}'")[0]

        if current_user.access_level >= 2:
            #Admin update
            client_id = db.get_user(f"WHERE user_name = '{form.member_name.data}'")[0]
            prof_id = db.get_user(f"WHERE user_name = '{ form.prof_name.data}'")[0]

            db.update_appointment(appointment_id=appt[0], status=form.status.data,
                                  date_appointment=form.date_appointment.data,
                                  slot=form.slot.data, venue=form.venue.data, client_id=client_id,
                                  professional_id=prof_id, service_id=service_id)
            
        else:
            #Member update
            db.update_appointment(appointment_id=appt[0], status=form.status.data,
                                  date_appointment=form.date_appointment.data,
                                  slot=form.slot.data, venue=form.venue.data, service_id=service_id)
        db.add_log(f"Updated appointment ID {appt[0]}", date.today(), "Appointments", current_user.user_name, current_user.user_id)
        flash("You have successfully updated the appointment!", "success")
        if current_user.access_level >=2:
            return redirect(url_for('administration.admin_appointments'))
        return redirect(url_for('appointment.appointment_view', appointment_id=appt[0]))
    return render_template('update-appointment.html', current_user=current_user, form=form)
