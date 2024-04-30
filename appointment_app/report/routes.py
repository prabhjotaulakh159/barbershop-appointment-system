from flask import Blueprint, render_template, flash, url_for, redirect
from appointment_app.qdb.database import db
from appointment_app.report.forms import AddReportForm
from datetime import date
from flask_login import login_required, current_user

report = Blueprint('report', __name__, template_folder="templates")
    
@report.route("/report/<int:appointment_id>", methods=['GET', 'POST'])
@login_required
def update_report(appointment_id):
    form = AddReportForm()
    if not db.check_if_appointment_already_has_report(appointment_id=appointment_id):
        db.add_report(None, None, date.today(), appointment_id)
    report = db.get_report(appointment_id)
    form.feedback_client.data = report[0]
    form.feedback_professional.data = report[1]
    if form.validate_on_submit():
        db.update_report(appointment_id=appointment_id, feedback_client=form.feedback_client.data, feedback_professional=form.feedback_professional.data)
        return redirect(url_for('appointment.my_appointments'))
    return render_template('update-report.html', form=form, current_user=current_user)