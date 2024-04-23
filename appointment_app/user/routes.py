from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from appointment_app.qdb.database import db
from appointment_app.user.forms import RegisterUserForm, LoginForm
from flask_login import login_user
from appointment_app.user.auth_config import User

user = Blueprint('user', __name__, template_folder="templates")


# @user.route("/login-client", methods=['GET', 'POST'])
# def login_client():
#     '''Renders the login client form'''
#     form = LoginForm()
#     if form.validate_on_submit():
#         client = db.get_client(form.username.data)
#         if not client:
#             flash(f"Client {form.username.data} does not exist")
#             return redirect(url_for('user.login_client'))
#         encrypted_password = client[2]
#         bcrypt = Bcrypt()
#         if not bcrypt.check_password_hash(encrypted_password, form.password.data):
#             flash("You provided invalid credentials")
#             return redirect(url_for('user.login'))
#         logged_in_client = User(
#             client_id=client[0], username=client[1], password=client[2], email=client[3], avatar=client[4], phone=client[5])
#         login_user(logged_in_client)
#         flash("You have sucessfully logged in !", "success")
#         return redirect(url_for('main.home'))
#     return render_template('login-client.html', form=form)


@user.route("/register", methods=["GET", "POST"])
def register():
    '''function rendering for the route /register'''
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        user_exist = db.get_user(username)
        if user_exist:
            flash(f'{username} already in db. Choose another username', 'error')
            return redirect(url_for('user.register'))
        b = Bcrypt()
        username = form.username.data
        password = b.generate_password_hash(form.password.data).decode('utf-8')
        email = form.email.data
        avatar = "/static/images/avatar.png"
        phone = form.phone.data
        payrate = form.pay_rate.data
        speciality = form.specialty.data
        address = form.address.data
        age = form.age.data
        usertype = form.user_type.data
        db.add_user(usertype,username, password, email,
                            avatar, phone, address,age, payrate, speciality)
        
        flash(f'Welcome {username} you are now a user', 'success')
        return redirect(url_for('main.home'))
    return render_template("register.html", form=form)


@user.route('/login-professional', methods=['GET', 'POST'])
def login_professional():
    '''renders register login from'''
    form = LoginForm()
    if form.validate_on_submit():
        professional = db.get_professional(form.username.data)
        if not professional:
            flash(f"Professional {form.username.data} does not exist !", "error")
            return redirect(url_for('user.login_professional'))
        bcrypt = Bcrypt()
        encrypted_password = professional[2]
        if not bcrypt.check_password_hash(encrypted_password, form.password.data):
            flash("You provided invalid credentials")
            return redirect(url_for('user.login'))
        logged_in_professional = Professional(
            professional_id=professional[0],
            username=professional[1],
            password=professional[2],
            email=professional[3], 
            avatar=professional[4], 
            phone=professional[5],
            pay_rate=professional[6],
            speciality=professional[7]
        )
        login_user(logged_in_professional)
        flash("You have successfully logged in !", "success")
        return redirect(url_for('main.home'))
    return render_template('login-professional.html', form=form)