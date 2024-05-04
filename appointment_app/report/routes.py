'''import flask and its methods'''
from datetime import date
from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import login_required, current_user
from appointment_app.qdb.database import db
from appointment_app.report.forms import AddReportForm

report = Blueprint('report', __name__, template_folder="templates")

@report.route("/report/<int:appointment_id>", methods=['GET', 'POST'])
@login_required
def update_report(appointment_id):
    '''function updating a specific report with appointment_id'''
    appointment = db.get_appointment(f"WHERE appointment_id = {appointment_id}")
    if current_user.user_id not in (appointment[5], appointment[6]) and current_user.access_level < 2:
        return redirect(url_for('main.home'))
    if not db.check_if_appointment_already_has_report(
            appointment_id=appointment_id):
        db.add_report(None, None, date.today(), appointment_id)
    form = AddReportForm()
    if form.validate_on_submit():
        if current_user.user_type == 'Member':
            db.update_client_report(form.feedback.data, appointment_id)
        else:
            db.update_professional_report(form.feedback.data, appointment_id)
        flash("Successfully added report !", "Success")
        return redirect(url_for('appointment.my_appointments'))
    return render_template('update-report.html', form=form, current_user=current_user)
