''' Routes for user auth '''
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
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        userdb = db.get_user(f"WHERE user_name = '{form.username.data}'")
        if not userdb:
            flash("You provided invalid credentials", "error")
            return redirect(url_for('user.login'))
        if userdb[1] == 0:
            flash("Your account is locked, please get in touch with an administrator", "error")
            return redirect(url_for('user.login'))
        bcrypt = Bcrypt()
        if not bcrypt.check_password_hash(userdb[5], form.password.data):
            flash("You provided invalid credentials", "error")
            return redirect(url_for('user.login'))
        userdb = User(userdb[0], userdb[1], userdb[2], userdb[3], userdb[4], userdb[5], userdb[6], userdb[7], userdb[8], userdb[9], userdb[10], userdb[11], userdb[12])
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
        user_exist = db.get_user(f"WHERE user_name = '{form.username.data}'")
        if user_exist:
            flash(f'{form.username.data} taken, choose another username', 'error')
            return redirect(url_for('user.register'))
        bcrypt = Bcrypt()
        avatar = '/images/avatar.png'
        if form.avatar.data:
            avatar = '/images/' + save_file(form.avatar.data)
        if form.user_type.data == "Member":
            form.pay_rate.data = None
            form.specialty.data = None
        db.add_user(form.user_type.data, form.username.data, bcrypt.generate_password_hash(form.password.data).decode("utf-8"), form.email.data, avatar, form.phone.data, form.address.data, form.age.data, form.pay_rate.data, form.specialty.data)
        flash(f'Welcome {form.username.data} you are now a user', 'success')
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
            user_already_exists = db.get_user(f"WHERE user_name = '{form.username.data}'")
            if user_already_exists:
                flash("Username already taken !", "error")
                return redirect(url_for('user.login'))
        new_avatar = current_user.avatar
        if form.avatar.data:
            new_avatar = '/images/' + save_file(form.avatar.data)
        db.update_user(user_id, form.username.data, form.email.data, new_avatar, form.phone.data, form.address.data, form.age.data, form.pay_rate.data, form.specialty.data)
        flash("You have successfully upated your profile !", "success")
        return redirect(url_for('main.home'))
    return render_template('update-profile.html', current_user=current_user, form=form)


@user.route("/update-user/<int:user_id>", methods=["GET", "POST"])
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
                return redirect(url_for('user.login'))
        current_avatar = userdb[7]
        if form.avatar.data:
            current_avatar = '/images/' + save_file(form.avatar.data)
        db.update_user(user_id, form.username.data, form.email.data, current_avatar, form.phone.data, form.address.data, form.age.data, form.pay_rate.data, form.specialty.data)
        flash("Successfully updated user", "success")
        return redirect(url_for('user.user_admin_panel'))
    return render_template('update-user.html', form=form, user=userdb)


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
            return redirect(url_for('user.change_password', user_id=current_user.user_id))
        new_password = form.confirm_new_password.data
        encrypted_new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.change_password(user_id, encrypted_new_password)
        logout_user()
        flash("You have successfully updated your password !", "success")
        return redirect(url_for('user.login'))
    return render_template('change-password.html', form=form)


@user.route("/all-users", methods=['GET', 'POST'])
@login_required
def user_admin_panel():
    ''' Loads user admin panel '''
    if current_user.access_level != 1:
        return redirect(url_for('main.home'))
    form = RegisterUserForm()
    users = db.get_all_users()
    if form.validate_on_submit():
        user_exist = db.get_user(f"WHERE user_name = '{form.username.data}'")
        if user_exist:
            flash(f'{form.username.data} taken, choose another username', 'error')
            return redirect(url_for('user.user_admin_panel', users=users, form=form))
        bcrypt = Bcrypt()
        avatar = '/images/avatar.png'
        if form.avatar.data:
            avatar = '/images/' + save_file(form.avatar.data)
        if form.user_type.data == "Member":
            form.pay_rate.data = None
            form.specialty.data = None
        db.add_user(form.user_type.data, form.username.data, bcrypt.generate_password_hash(form.password.data).decode("utf-8"), form.email.data, avatar, form.phone.data, form.address.data, form.age.data, form.pay_rate.data, form.specialty.data)
        flash('User has been created !', 'success')
        return redirect(url_for('user.user_admin_panel', users=users, form=form))
    return render_template('user-admin-panel.html', users=users, form=form)


@user.route("/delete-user/<int:user_id>")
@login_required
def delete_user(user_id):
    ''' Admins can delete a user by their ID '''
    if current_user.access_level not in (1, 3):
        return redirect(url_for('main.home'))
    if user_id == current_user.user_id:
        return redirect(url_for('user.all_users'))
    db.delete_user(user_id)
    flash("User deleted", "success")
    return redirect(url_for('user.user_admin_panel'))
   

@user.route("/disable-user/<int:user_id>")
@login_required
def toggle_activation(user_id):
    ''' Admins can disable a user '''
    if current_user.access_level not in (1,3):
        return redirect(url_for('main.home'))
    if user_id == current_user.user_id:
        return redirect(url_for('main.home'))
    db.toggle_enable_disable(user_id)
    flash("User has been disabled", "success")
    return redirect(url_for('user.user_admin_panel'))