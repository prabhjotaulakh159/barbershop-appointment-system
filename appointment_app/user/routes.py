''' Routes for user auth '''

from datetime import date
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, login_required, logout_user

from appointment_app.user.auth_config import User
from appointment_app.user.utils import save_file
from appointment_app.qdb.database import db
from appointment_app.user.forms import RegisterUserForm, LoginForm, ChangePasswordForm


user = Blueprint('user', __name__, template_folder="templates", static_folder="static", static_url_path='/static/user')


@user.route("/login", methods=['GET', 'POST'])
def login():
    ''' Logs in a user '''
    # if already logged in, then redirect back to home
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():

        # check if user exists
        user_from_db = db.get_user(f"WHERE user_name = '{form.username.data}'")        
        if not user_from_db:
            flash("You provided invalid credentials", "error")
            return redirect(url_for('user.login'))

        # check if account is locked
        if user_from_db[1] == 0:
            flash("Your account is locked, please get in touch with an administrator", "error")
            return redirect(url_for('user.login'))

        # validate credentials
        valid_password = Bcrypt().check_password_hash(user_from_db[5], form.password.data)
        if not valid_password:
            flash("You provided invalid credentials", "error")
            return redirect(url_for('user.login'))

        # login user
        authenticated_user = User(user_from_db[0], user_from_db[1], user_from_db[2], user_from_db[3], user_from_db[4], user_from_db[5], user_from_db[6], user_from_db[7], user_from_db[8], user_from_db[9], user_from_db[10], user_from_db[11], user_from_db[12], user_from_db[13])
        login_user(authenticated_user)

        # display warnings if any
        if user_from_db[13] != 0:
            flash(f"You have {user_from_db[13]} warnings, please be careful", "warning")
        else:
            flash("You have sucessfully logged in !", "success")
        db.add_log(f"User {current_user.user_name} logged in", date.today(), "None", current_user.user_name, current_user.user_id)
        # login successful, redirect to home
        return redirect(url_for('main.home'))
    
    return render_template('login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    ''' Logs out a user '''
    db.add_log(f"User {current_user.user_name} logged out", date.today(), "None", current_user.user_name, current_user.user_id)
    logout_user()
    flash("You have been logged out", "success")
    
    return redirect(url_for('user.login'))


@user.route("/register", methods=["GET", "POST"])
def register():
    '''function rendering for the route /register'''
    # if logged in, redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegisterUserForm()
    if form.validate_on_submit():

        # check if username is taken
        user_exist = db.get_user(f"WHERE user_name = '{form.username.data}'")
        if user_exist:
            flash(f'{form.username.data} taken, choose another username', 'error')
            return redirect(url_for('user.register'))

        # register profile picture if provided, else
        # simply use the default profile picture
        if form.avatar.data:
            avatar = '/images/' + save_file(form.avatar.data)
        else:
            avatar = '/images/avatar.png'

        # dont insert professional fields if member
        if form.user_type.data == "Member":
            form.pay_rate.data = None
            form.specialty.data = None
            
        # Professional must be 18
        if form.user_type.data == "Professional" and form.age.data < 18:
            flash("Professionals must be at least 18 years old", "error")
            return redirect(url_for('user.register'))

        # hash password and create account
        encrypted_password = Bcrypt().generate_password_hash(form.password.data).decode("utf-8")
        
        db.add_user(form.user_type.data, form.username.data, encrypted_password, form.email.data, avatar, form.phone.data, form.address.data, form.age.data, form.pay_rate.data, form.specialty.data)
        flash(f'Welcome {form.username.data} you are now a user', 'success')
        user_id = db.get_user(f"WHERE user_name = '{form.username.data}'")
        db.add_log(f"New User '{form.username.data}' has registered", date.today(), "Users", form.username.data, user_id[0])
        return redirect(url_for('user.login'))

    return render_template("register.html", form=form)


@user.route("/update-profile/<int:user_id>", methods=['GET', 'POST'])
@login_required
def update_profile(user_id):
    ''' Updates a user '''
    # cannot update someone else account
    if current_user.user_id != user_id:
        return redirect(url_for('main.home'))

    form = RegisterUserForm()

    # fill in fields with current data
    if request.method == 'GET':
        form.username.data = current_user.user_name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.user_type.data = current_user.user_type
        form.age.data = current_user.age
        form.address.data = current_user.address
        form.pay_rate.data = current_user.pay_rate
        form.specialty.data = current_user.specialty
    else:
        # if the username is different from the current one, we must
        # check if its unique
        if form.username.data != current_user.user_name:
            user_already_exists = db.get_user(f"WHERE user_name = '{form.username.data}'")
            if user_already_exists:
                flash("Username already taken !", "error")
                return redirect(url_for('user.login'))
    
        # check for profile pic change, else use the same one as before
        new_avatar = current_user.avatar
        if form.avatar.data:
            new_avatar = '/images/' + save_file(form.avatar.data)
    
        # update the user
        db.update_user(user_id, form.username.data, form.email.data, new_avatar, form.phone.data, form.address.data, form.age.data, form.pay_rate.data, form.specialty.data)
        flash("You have successfully updated your profile !", "success")
        db.add_log(f"Updated User {form.username.data}'s profile", date.today(), "Users", current_user.user_name, current_user.user_id)
        return redirect(url_for('main.home'))

    return render_template('update-profile.html', current_user=current_user, form=form)


@user.route("/change-password/<int:user_id>", methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    ''' Changes a users password '''
    # cannot change someone else's password
    if current_user.user_id != user_id:
        return redirect(url_for('main.home'))
    
    form = ChangePasswordForm()
    if form.validate_on_submit():
        userdb = db.get_user(f"WHERE user_name = '{current_user.user_name}'")
        bcrypt = Bcrypt()
        
        # check if current password is correct during re-login
        if not bcrypt.check_password_hash(userdb[5], form.old_password.data):
            flash("You have provided invalid credentials !", "error")
            return redirect(url_for('user.change_password', user_id=current_user.user_id))
        
        # change the password after authentication
        new_password = form.confirm_new_password.data
        encrypted_new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.change_password(user_id, encrypted_new_password)
        
        # they must log back in
        db.add_log(f"Updated User {current_user.user_name}'s password", date.today(), "Users", current_user.user_name, current_user.user_id)
        logout_user()
        flash("You have successfully updated your password !", "success")
        
        return redirect(url_for('user.login'))
    
    return render_template('change-password.html', form=form)

