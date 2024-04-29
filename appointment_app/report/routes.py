from flask import Blueprint, render_template, flash, url_for, redirect
from appointment_app.qdb.database import db
from appointment_app.report.forms import AddReportForm
from datetime import date
from flask_login import login_required

report = Blueprint('report', __name__, template_folder="templates")

@report.route('/report/<int:appointment_id>')
@login_required
def add_report(appointment_id):
    form = AddReportForm()
    if form.validate_on_submit():
    	db.add_report(form.feedback_client.data, form.feedback_professional.data, date.today(), appointment_id)
    	flash("Your report has been successfully added !", "success")
    	return redirect(url_for('appointment.all_appointments'))
    return render_template('add-report.html', form=form)

