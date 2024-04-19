from flask import Blueprint, render_template, flash, redirect
from flask_bcrypt import Bcrypt
from appointment_app.qdb.database import Database
from appointment_app.user.client import Member
from appointment_app.user.forms import RegisterMemberForm


user = Blueprint('user', __name__, template_folder="templates",
                 static_folder="static")


@user.route("/register", methods=["GET", "POST"])
def register():
    '''function rendering for the route /register'''
    form = RegisterMemberForm()
    context_data = {"page_title": "Registration"}
    if form.validate_on_submit():
        username = form.username.data
        user_exist = db.get_client(username)
        if user_exist:
            flash(f'{username} already in db. Choose another username', 'error')
        else:
            b = Bcrypt()
            username = form.username.data
            password = b.generate_password_hash(
                form.password.data).decode('utf-8')
            email = form.email.data
            #avatar = form.avatar.data
            phone = form.phone.data
            db.add_client(username, password, email, avatar, phone)
            flash(f'Welcome {username} you are now a client', 'success')
            return redirect(url_for('user.login'))
    return render_template("registration.html", context=context_data, form=form)
