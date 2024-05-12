'''import flask and its methods'''
from datetime import date
from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_bcrypt import Bcrypt
from flask_login import login_required, current_user
from appointment_app.qdb.database import db
from appointment_app.appointment.forms import AppointmentForm, AppointmentAdminForm
from appointment_app.appointment.utility import time_slots, venues, appointment_status
from appointment_app.user.auth_config import User
from appointment_app.user.utils import save_file
from appointment_app.user.forms import RegisterUserForm, LoginForm, ChangePasswordForm
from appointment_app.administration.forms import AdminCrudForm

administration = Blueprint('administration', __name__, template_folder="templates",
                 static_folder="static", static_url_path="/static/administration")

@administration.route('/admin-appointments', methods=["GET", "POST"])
@login_required
def admin_appointments():
    '''function to add and list all appointments for admin_appoint'''
    
    if current_user.access_level < 2:
        return redirect(url_for('main.home'))
    form = AppointmentAdminForm()

    members = db.get_users("WHERE user_type = 'Member'")
    members_list = []
    for member in members:
        members_list.append((member[4], member[4]))

    services = db.get_services()
    services_list = []
    for service in services:
        services_list.append((service[1], service[1]))

    professionals = db.get_users("WHERE user_type = 'Professional'")
    professionals_list = []
    for professional in professionals:
        professionals_list.append((professional[4], professional[4]))

    form.member_name.choices = members_list
    form.prof_name.choices = professionals_list
    form.service.choices = services_list
    form.slot.choices = time_slots
    form.venue.choices = venues
    form.status.choices = appointment_status
    if form.validate_on_submit():

        status = form.status.data
        client_id = db.get_user(f"WHERE user_name = '{form.member_name.data}'")[0]
        prof_id = db.get_user(f"WHERE user_name = '{form.prof_name.data}'")[0]
        service_id = db.get_service(f"WHERE service_name = '{form.service.data}'")[0]
        db.add_appointment(status, form.date_appointment.data,
                           form.slot.data, form.venue.data, client_id, prof_id, service_id)
        db.add_log(f"Created new appointment for client {form.member_name.data}", date.today(), "Appointments", current_user.user_name, current_user.user_id)
        
        flash('Appointment is created!','success')

    order_by = request.args.get('order_by')
    cond = None
    if order_by:
        cond = f"ORDER BY {order_by}"
    
    appointments = db.get_appointments(cond)
    names = []
    reports = []
    for apt in appointments:
        client_name = db.get_user(f"WHERE user_id= {apt[5]}")
        professional_name = db.get_user(f"WHERE user_id = {apt[6]}")
        service_name = db.get_service(f"WHERE service_id = {apt[7]}")

        names.append((client_name[4], professional_name[4], service_name[1]))
        reports.append(db.get_report(apt[0]))
        
    return render_template("admin-appointments.html", form=form,
                           appointments=appointments, names=names, reports=reports)


@administration.route('/delete-appointment/<int:appointment_id>')
@login_required
def delete_appointment(appointment_id):
    '''function deleting specific appointment with appointment_id'''
    if current_user.access_level < 2:
        return redirect(url_for('main.home'))

    db.delete_appointment(appointment_id)
    db.add_log(f"Deleted appointment ID {appointment_id}", date.today(), "Appointments", current_user.user_name, current_user.user_id)
    flash("Appointment is deleted!", 'success')
    return redirect(url_for('administration.admin_appointments'))

@administration.route('/admin-logs')
@login_required
def view_logs():
    '''function to list all logs '''
    if current_user.access_level < 2:
        return redirect(url_for('main.home'))
    
    logs = db.get_logs(f"ORDER BY log_id")
    return render_template("admin-logs.html", logs=logs)


@administration.route('/view-admins', methods=['GET', 'POST'])
@login_required
def view_admins():
    '''lists all admins'''
    if current_user.access_level != 3:
        return redirect(url_for('main.home'))
    form = AdminCrudForm()
    admins = db.get_all_admins()
    return render_template('view-admins.html', form=form, admins=admins)