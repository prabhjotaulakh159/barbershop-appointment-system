from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from appointment_app.qdb.database import db
from appointment_app.user.forms import RegisterClientForm


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
        else:
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
