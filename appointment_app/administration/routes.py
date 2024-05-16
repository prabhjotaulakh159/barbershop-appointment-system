'''import flask and its methods'''
from datetime import date
from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_bcrypt import Bcrypt
from flask_login import login_required, current_user
from appointment_app.qdb.database import db
from appointment_app.appointment.forms import AppointmentAdminForm
from appointment_app.appointment.utility import time_slots, venues, appointment_status
from appointment_app.user.utils import save_file
from appointment_app.user.forms import RegisterUserForm
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
        services_list.append((service[1], service[1]+" "+str(service[3])+"$"))

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

    #fill the condition before getting the appointments
    order_by = request.args.get('order_by')
    order_by_cond = None
    if order_by:
        order_by_cond = f"ORDER BY a4.{order_by}"

    appointments = db.get_appts_with_joins(order_by_cond)
    return render_template("admin-appointments.html", form=form, appointments=appointments)


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
    
    logs = db.get_logs("ORDER BY log_id")
    return render_template("admin-logs.html", logs=logs)


@administration.route("/update-user/<int:user_id>", methods=["GET", "POST"])
@login_required
def update_user(user_id):
    ''' Admin updates another user '''
    if current_user.user_type != 'Admin' or current_user.access_level not in (1, 3) or user_id == current_user.user_id:
        return redirect(url_for('main.home'))
    userdb = db.get_user(f"WHERE user_id = {user_id}")
    form = RegisterUserForm()
    if request.method == 'GET':
        form.username.data = userdb[4]
        form.email.data = userdb[6]
        form.phone.data = userdb[8]
        form.user_type.data = userdb[3]
        form.age.data = userdb[10]
        form.address.data = userdb[9]
        form.pay_rate.data = userdb[11]
        form.specialty.data = userdb[12]
    else:
        if form.username.data != userdb[4]:
            user_already_exists = db.get_user(f"WHERE user_name = '{form.username.data}'")
            if user_already_exists:
                flash("Username already taken !", "error")
                return redirect(url_for('administration.update_user'))
        current_avatar = userdb[7]
        if form.avatar.data:
            current_avatar = '/images/' + save_file(form.avatar.data)
        db.update_user(user_id, form.username.data, form.email.data, current_avatar, form.phone.data, form.address.data, form.age.data, form.pay_rate.data, form.specialty.data)
        db.add_log(f"Updated user profile for user '{form.username.data}'", date.today(), "Users", current_user.user_name, current_user.user_id)
        flash("Successfully updated user", "success")
        if '/view-admins' in request.referrer:
            return redirect(url_for('administration.view_admins'))
        return redirect(url_for('administration.user_admin_panel'))
    return render_template('update-user.html', form=form, user=userdb)


@administration.route("/user-admin-panel", methods=['GET', 'POST'])
@login_required
def user_admin_panel():
    ''' Loads user admin panel '''
    if current_user.access_level != 1 and current_user.access_level != 3:
        return redirect(url_for('main.home'))
    form = RegisterUserForm()
    users = db.get_all_users()
    if form.validate_on_submit():
        user_exist = db.get_user(f"WHERE user_name = '{form.username.data}'")
        if user_exist:
            flash(f'{form.username.data} taken, choose another username', 'error')
            return redirect(url_for('administration.user_admin_panel', users=users, form=form))
        bcrypt = Bcrypt()
        avatar = '/images/avatar.png'
        if form.avatar.data:
            avatar = '/images/' + save_file(form.avatar.data)
        if form.user_type.data == "Member":
            form.pay_rate.data = None
            form.specialty.data = None
        db.add_user(form.user_type.data, form.username.data, bcrypt.generate_password_hash(form.password.data).decode("utf-8"), form.email.data, avatar, form.phone.data, form.address.data, form.age.data, form.pay_rate.data, form.specialty.data)
        db.add_log(f"Created new user '{form.username.data}'", date.today(), "Users", current_user.user_name, current_user.user_id)
        flash('User has been created !', 'success')
        return redirect(url_for('administration.user_admin_panel', users=users, form=form))
    return render_template('user-admin-panel.html', users=users, form=form)

@administration.route("/delete-user/<int:user_id>")
@login_required
def delete_user(user_id):
    ''' Admins can delete a user by their ID '''
    if current_user.access_level not in (1, 3):
        return redirect(url_for('main.home'))
    if user_id == current_user.user_id:
        return redirect(url_for('administration.user_admin_panel'))
    db.delete_user(user_id)
    if current_user.access_level in (1,3):
        db.add_log(f"Deleted user ID '{user_id}'", date.today(), "Users", current_user.user_name, current_user.user_id)
    flash("User deleted", "success")
    # check if deletion was from view admins or view users, and 
    # redirect accordingly 
    if '/view-admins' in request.referrer:
        return redirect(url_for('administration.view_admins'))
    return redirect(url_for('administration.user_admin_panel'))
        


@administration.route("/disable-user/<int:user_id>")
@login_required
def toggle_activation(user_id):
    ''' Admins can disable a user '''
    if current_user.access_level not in (1,3):
        return redirect(url_for('main.home'))
    if user_id == current_user.user_id:
        return redirect(url_for('main.home'))
    db.toggle_enable_disable(user_id)
    user = db.get_user(f"WHERE user_id = {user_id}")
    print(user[1])
    if user[1] is 0:
        db.add_log(f"Disabled user ID '{user_id}'", date.today(), "Users", current_user.user_name, current_user.user_id)
        flash("User has been disabled", "success")
    else:
        db.add_log(f"Enabled user ID '{user_id}'", date.today(), "Users", current_user.user_name, current_user.user_id)
        flash("User has been enabled", "success")
    if '/view-admins' in request.referrer:
        return redirect(url_for('administration.view_admins'))
    return redirect(url_for('administration.user_admin_panel'))

@administration.route("/warn-user/<int:user_id>")
@login_required
def warn_user(user_id):
    '''admins can warn users'''
    if current_user.access_level not in (1,3):
        return redirect(url_for('main.home'))
    if user_id == current_user.user_id:
        return redirect(url_for('main.home'))
    db.warn_user(user_id)
    flash("You successfully warned the user", "success")
    if '/view-admins' in request.referrer:
        return redirect(url_for('administration.view_admins'))
    return redirect(url_for('administration.user_admin_panel'))

@administration.route('/view-admins', methods=['GET', 'POST'])
@login_required
def view_admins():
    '''lists all admins'''
    if current_user.access_level != 3:
        return redirect(url_for('main.home'))
    form = AdminCrudForm()
    admins = db.get_all_admins()
    if form.validate_on_submit():
        user_exist = db.get_user(f"WHERE user_name = '{form.username.data}'")
        if user_exist:
            flash(f'{form.username.data} taken, choose another username', 'error')
            return redirect(url_for('administration.view_admins'))
        bcrypt = Bcrypt()
        avatar = '/images/avatar.png'
        if form.avatar.data:
            avatar = '/images/' + save_file(form.avatar.data)
        if form.user_type.data == "Member":
            form.pay_rate.data = None
            form.specialty.data = None
        if form.user_type.data == 'Admin User':
            access_level = 1
        else:
            access_level = 2
        db.add_admin(
            access_level=access_level,
            user_name=form.username.data,
            pass_word=bcrypt.generate_password_hash(form.password.data),
            email=form.email.data,
            avatar=avatar,
            phone=form.phone.data,
            age=form.age.data,
            address=form.address.data
        )
        flash('Admin has been created', 'success')
        return redirect(url_for('administration.view_admins'))
    return render_template('view-admins.html', form=form, admins=admins)


@administration.route("/toggle-access-level/<int:user_id>")
@login_required
def toggle_access_level(user_id):
    '''Changes an admins access level to switch between admin user or admin appointment'''
    if current_user.access_level != 3:
        return redirect(url_for('main.home'))
    if user_id == current_user.user_id:
        return redirect(url_for('main.home'))
    db.toggle_access_level(user_id=user_id)
    flash("Successfully switched access level", "success")
    return redirect(url_for("administration.view_admins"))