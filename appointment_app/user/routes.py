from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from appointment_app.qdb.database import db
from appointment_app.user.forms import RegisterUserForm, LoginForm
from flask_login import login_user
from appointment_app.user.auth_config import User

user = Blueprint('user', __name__, template_folder="templates")


@user.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        client = db.get_user(form.username.data)
        if not client:
            flash(f"You provided invalid credentials")
            return redirect(url_for('user.login_client'))
        user_id = client[0]
        is_active = client[1]
        access_level = client[2]
        user_name = client[3]
        pass_word = client[4] # this is encrypted
        email = client[5]
        avatar = client[6]
        phone = client[7]
        address = client[8]
        age = client[9]
        pay_rate = client[10]
        specialty = client[12]
        bcrypt = Bcrypt()
        if not bcrypt.check_password_hash(pass_word, form.password.data):
            flash("You provided invalid credentials")
            return redirect(url_for('user.login'))
        user = User(user_id, is_active, access_level, user_name, email, avatar, phone, address, age, pay_rate, specialty)
        login_user(user)
        flash("You have sucessfully logged in !", "success")
        return redirect(url_for('main.home'))
    return render_template('login.html', form=form)


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
        db.add_user(username, password, email,
                            avatar, phone, payrate, speciality)
        flash(f'Welcome {username} you are now a professional', 'success')
        return redirect(url_for('main.home'))
    return render_template("register.html", form=form)