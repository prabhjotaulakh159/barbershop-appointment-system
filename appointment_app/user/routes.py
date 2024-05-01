''' Routes for user auth '''
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, login_required, logout_user
from appointment_app.user.auth_config import User
from appointment_app.user.utils import save_file
from appointment_app.qdb.database import db
from appointment_app.user.forms import (RegisterUserForm,
                                        LoginForm,
                                        ChangePasswordForm)


user = Blueprint('user', __name__, template_folder="templates")


@user.route("/login", methods=['GET', 'POST'])
def login():
    ''' Logs in a user '''
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        userdb = db.get_user(f"WHERE user_name = '{form.username.data}'")
        if not userdb:
            flash("You provided invalid credentials", "error")
            return redirect(url_for('user.login'))
        user_id = userdb[0]
        is_enabled = userdb[1]
        access_level = userdb[2]
        user_type = userdb[3]
        user_name = userdb[4]
        pass_word = userdb[5]
        email = userdb[6]
        avatar = userdb[7]
        phone = userdb[8]
        address = userdb[9]
        age = userdb[10]
        pay_rate = userdb[11]
        specialty = userdb[12]
        bcrypt = Bcrypt()
        if not bcrypt.check_password_hash(pass_word, form.password.data):
            flash("You provided invalid credentials", "error")
            return redirect(url_for('user.login'))
        userdb = User(user_id, is_enabled, access_level, user_type,
                      user_name, pass_word, email, avatar, phone, address,
                      age, pay_rate, specialty)
        login_user(userdb)
        flash("You have sucessfully logged in !", "success")
        return redirect(url_for('main.home'))
    return render_template('login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    ''' Logs out a user '''
    logout_user()
    flash("You have been logged out", "success")
    return redirect(url_for('user.login'))


@user.route("/register", methods=["GET", "POST"])
def register():
    '''function rendering for the route /register'''
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        user_exist = db.get_user(f"WHERE user_name = '{username}'")
        if user_exist:
            flash(f'{username} takne, choose another username', 'error')
            return redirect(url_for('user.register'))
        b = Bcrypt()
        usertype = form.user_type.data
        username = form.username.data
        password = b.generate_password_hash(form.password.data).decode('utf-8')
        email = form.email.data
        avatar = '/images/avatar.png'
        if form.avatar.data:
            avatar = '/images/' + save_file(form.avatar.data)
        phone = form.phone.data
        address = form.address.data
        age = form.age.data
        if usertype == "Member":
            payrate = None
            speciality = None
        else:
            payrate = form.pay_rate.data
            speciality = form.specialty.data
        db.add_user(usertype, username, password, email,
                    avatar, phone, address, age, payrate, speciality)
        flash(f'Welcome {username} you are now a user', 'success')
        return redirect(url_for('user.login'))
    return render_template("register.html", form=form)


@user.route("/update-profile/<int:user_id>", methods=['GET', 'POST'])
@login_required
def update_profile(user_id):
    ''' Updates a user '''
    if current_user.user_id != user_id:
        return redirect(url_for('main.home'))
    form = RegisterUserForm()
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
        if form.username.data != current_user.user_name:
            user_already_exists = db.get_user(
                f"WHERE user_name = '{form.username.data}'")
            if user_already_exists:
                flash("Username already taken !", "error")
                return redirect(url_for('user.login'))
        new_avatar = current_user.avatar
        if form.avatar.data:
            new_avatar = '/images/' + save_file(form.avatar.data)
        db.update_user(user_id, form.username.data, form.email.data,
                       new_avatar, form.phone.data, form.address.data,
                       form.age.data, form.pay_rate.data, form.specialty.data)
        flash("You have successfully upated your profile !", "success")
        return redirect(url_for('main.home'))
    return render_template('update-profile.html', current_user=current_user,
                           form=form)


@user.route("/change-password/<int:user_id>", methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    ''' Changes a users password '''
    if current_user.user_id != user_id:
        return redirect(url_for('main.home'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        userdb = db.get_user(f"WHERE user_name = '{current_user.user_name}'")
        bcrypt = Bcrypt()
        if not bcrypt.check_password_hash(userdb[5], form.old_password.data):
            flash("You have provided invalid credentials !", "error")
            return redirect(url_for('user.change_password',
                                    user_id=current_user.user_id))
        new_password = form.confirm_new_password.data
        encrypted_new_password = bcrypt.generate_password_hash(new_password)
        encrypted_new_password = encrypted_new_password.decode('utf-8')
        db.change_password(user_id, encrypted_new_password)
        logout_user()
        flash("You have successfully updated your password !", "success")
        return redirect(url_for('user.login'))
    return render_template('change-password.html', form=form)


@user.route("/all-users", methods=['GET', 'POST'])
@login_required
def all_users():
    ''' Gets all users from the db'''
    users = db.get_all_users()
    return render_template('all-users.html', users=users)
