'''import flask and its methods'''
from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_bcrypt import Bcrypt
from flask_login import login_required, current_user
from appointment_app.qdb.database import db
from appointment_app.appointment.forms import AppointmentForm, AppointmentAdminForm
from appointment_app.appointment.utility import time_slots, venues
from appointment_app.user.auth_config import User
from appointment_app.user.utils import save_file
from appointment_app.user.forms import RegisterUserForm, LoginForm, ChangePasswordForm

administration = Blueprint('administration', __name__, template_folder="templates",
                 static_folder="static", static_url_path="/static/administration")

# @administration.route("/dashboard", methods=['GET', 'POST'])
# def dashboard():
#     if current_user.access_level != 3:
#         return redirect(url_for('main.home'))
    
#     appointment_form = AppointmentAdminForm()
#     user_form = RegisterUserForm()
    
#     # Get data for appointment_form
#     members = db.get_users("WHERE user_type = 'Member'")
#     members_list = []
#     for member in members:
#         members_list.append((member[4], member[4]))

#     services = db.get_services()
#     services_list = []
#     for service in services:
#         services_list.append((service[1], service[1]))

#     professionals = db.get_users("WHERE user_type = 'Professional'")
#     professionals_list = []
#     for professional in professionals:
#         professionals_list.append((professional[4], professional[4]))

#     appointment_form.member_name.choices = members_list
#     appointment_form.prof_name.choices = professionals_list
#     appointment_form.service.choices = services_list
#     appointment_form.slot.choices = time_slots
#     appointment_form.venue.choices = venues
    
#     # Validate appointment_form
#     if appointment_form.validate_on_submit():
#         status = 1
#         client_id = db.get_user(f"WHERE user_name = '{appointment_form.member_name.data}'")[0]
#         prof_id = db.get_user(f"WHERE user_name = '{appointment_form.prof_name.data}'")[0]
#         service_id = db.get_service(f"WHERE service_name = '{appointment_form.service.data}'")[0]
#         db.add_appointment(status, appointment_form.date_appointment.data,
#                            appointment_form.slot.data, appointment_form.venue.data, client_id, prof_id, service_id)
#         flash('Appointment is created!','success')

#     # Validate user_form
#     if user_form.validate_on_submit():
#         user_exist = db.get_user(f"WHERE user_name = '{user_form.username.data}'")
#         if user_exist:
#             flash(f'{user_form.username.data} taken, choose another username', 'error')
#             return redirect(url_for('user.user_admin_panel'))
#         bcrypt = Bcrypt()
#         avatar = '/images/avatar.png'
#         if user_form.avatar.data:
#             avatar = '/images/' + save_file(user_form.avatar.data)
#         if user_form.user_type.data == "Member":
#             user_form.pay_rate.data = None
#             user_form.specialty.data = None
#         db.add_user(user_form.user_type.data, user_form.username.data, bcrypt.generate_password_hash(user_form.password.data).decode("utf-8"), user_form.email.data, avatar, user_form.phone.data, user_form.address.data, user_form.age.data, user_form.pay_rate.data, user_form.specialty.data)
#         flash('User has been created !', 'success')

#     # Get data for appointments
#     order_by = request.args.get('order_by')
#     cond = None
#     if order_by:
#         cond = f"ORDER BY {order_by}"
    
#     appointments = db.get_appointments(cond)
#     names = []
#     reports = []
#     for apt in appointments:
#         client_name = db.get_user(f"WHERE user_id= {apt[5]}")
#         professional_name = db.get_user(f"WHERE user_id = {apt[6]}")
#         service_name = db.get_service(f"WHERE service_id = {apt[7]}")

#         names.append((client_name[4], professional_name[4], service_name[1]))
#         reports.append(db.get_report(apt[0]))

#     # Get data for users
#     users = db.get_all_users()
    
#     return render_template("superadmin-dashboard.html", appointment_form=appointment_form,
#                            user_form=user_form,appointments=appointments, names=names, users=users,reports=reports, )