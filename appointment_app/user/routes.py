from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from appointment_app.qdb.database import Database
from appointment_app.user.forms import RegisterClientForm,RegisterProfessionalForm


user = Blueprint('user', __name__, template_folder="templates",
                 static_folder="static")

db = Database()

@user.route("/register/client", methods=["GET", "POST"])
def register():
    '''function rendering for the route /register'''
    form = RegisterClientForm()
    context_data = {"page_title": "Registration"}
    
    if form.validate_on_submit():
        username = form.username.data
        client_exist = db.get_client(username)
        if client_exist:
            flash(f'{username} already in db. Choose another username', 'error')
        else:
            b = Bcrypt()
            username = form.username.data
            password = b.generate_password_hash(form.password.data).decode('utf-8')
            email = form.email.data
            avatar = "/static/images/avatar.png" 
            phone = form.phone.data
            db.add_client(username, password, email, avatar, phone)
            flash(f'Welcome {username} you are now a client', 'success')
            #return redirect(url_for('user.login'))
            
    return render_template("registration-client.html", context=context_data, form=form)

@user.route("/register/professional", methods=["GET", "POST"])
def register_professional():
    '''function rendering for the route /register/professional'''
    form = RegisterProfessionalForm()
    context_data = {"page_title": "Registration"}
    
    if form.validate_on_submit():
        username = form.username.data
        client_exist = db.get_client(username)
        if client_exist:
            flash(f'{username} already in db. Choose another username', 'error')
        else:
            b = Bcrypt()
            username = form.username.data
            password = b.generate_password_hash(form.password.data).decode('utf-8')
            email = form.email.data
            avatar = "/static/images/avatar.png" 
            phone = form.phone.data
            payrate = form.payrate.data
            speciality = form.specialty.data
            db.add_professional(username, password, email, avatar, phone,payrate,speciality)
            flash(f'Welcome {username} you are now a professional', 'success')
            print("WORKED")
            #return redirect(url_for('user.login'))
            
    return render_template("registration-professional.html", context=context_data, form=form)
