from flask import Blueprint, render_template
from appointment_app.qdb.database import Database
from appointment_app.user.member import Member



user = Blueprint('user', __name__, template_folder="templates",
                 static_folder="static")


@owner.route("/register",methods=["GET","POST"])
def register():
    '''function rendering for the route /register'''
    form = NewOwnerForm()
    context_data = {"page_title":"Registration"}
    if form.validate_on_submit():
        username = form.username.data
        user_exist=db.get_owner(username)
        if user_exist:
            flash (f'{username} already in db. Choose another username','error')
        else:
            b=Bcrypt()
            username=form.username.data
            owner_name=form.owner_name.data
            email=form.email.data
            password=b.generate_password_hash(form.password.data).decode('utf-8')
            occupation=form.occupation.data
            db.add_new_owner(username,owner_name,email,password,occupation)
            flash (f'Welcome {username} you are now a owner','success')
            return redirect(url_for('owner.login'))
    return render_template("registration.html",context=context_data, form=form)