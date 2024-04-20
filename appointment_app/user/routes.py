from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from appointment_app.qdb.database import db
from appointment_app.user.forms import RegisterClientForm, LoginForm, RegisterProfessionalForm
from flask_login import login_user
from appointment_app.user.auth_config import Client, Professional

user = Blueprint('user', __name__, template_folder="templates")


@user.route("/register-client", methods=["GET", "POST"])
def register_client():
    '''function rendering for the route /register'''
    form = RegisterClientForm()
    if form.validate_on_submit():
        username = form.username.data
        client_exist = db.get_client(username)
        if client_exist:
            flash(f'{username} already in db. Choose another username', 'error')
            return redirect(url_for('user.register'))
        b = Bcrypt()
        username = form.username.data
        password = b.generate_password_hash(form.password.data).decode('utf-8')
        email = form.email.data
        avatar = "/static/images/avatar.png"
        phone = form.phone.data
        db.add_client(username, password, email, avatar, phone)
        flash(f'Welcome {username} you are now a client', 'success')
        return redirect(url_for('main.home'))
    return render_template("register-client.html", form=form)


@user.route("/login-client", methods=['GET', 'POST'])
def login_client():
    '''Renders the login client form'''
    form = LoginForm()
    if form.validate_on_submit():
        client = db.get_client(form.username.data)
        if not client:
            flash(f"Client {form.username.data} does not exist")
            return redirect(url_for('user.login_client'))
        encrypted_password = client[2]
        bcrypt = Bcrypt()
        if not bcrypt.check_password_hash(encrypted_password, form.password.data):
            flash("You provided invalid credentials")
            return redirect(url_for('user.login'))
        logged_in_client = Client(
            client_id=client[0], username=client[1], password=client[2], email=client[3], avatar=client[4], phone=client[5])
        login_user(logged_in_client)
        flash("You have sucessfully logged in !", "success")
        return redirect(url_for('main.home'))
    return render_template('login-client.html', form=form)


@user.route("/register-professional", methods=["GET", "POST"])
def register_professional():
    '''function rendering for the route /register/professional'''
    form = RegisterProfessionalForm()
    if form.validate_on_submit():
        username = form.username.data
        professional_exist = db.get_professional(username)
        if professional_exist:
            flash(f'{username} already in db. Choose another username', 'error')
            return redirect(url_for('user.register_professional'))
        b = Bcrypt()
        username = form.username.data
        password = b.generate_password_hash(form.password.data).decode('utf-8')
        email = form.email.data
        avatar = "/static/images/avatar.png"
        phone = form.phone.data
        payrate = form.payrate.data
        speciality = form.specialty.data
        db.add_professional(username, password, email,
                            avatar, phone, payrate, speciality)
        flash(f'Welcome {username} you are now a professional', 'success')
        return redirect(url_for('main.home'))
    return render_template("register-professional.html", form=form)


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