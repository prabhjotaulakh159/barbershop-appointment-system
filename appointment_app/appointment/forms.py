from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField, FloatField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo


class AppointmentForm(FlaskForm):
    date_appointment = DateField(
        "Date", format='%Y-%m-%d', validators=[DataRequired()])

    slot = SelectField("Time Slot", choices=[
        ('10-11', '10am - 11am'),
        ('11-12', '11am - 12pm'),
        ('12-1', '12pm - 1pm'),
        ('1-2', '1pm - 2pm'),
        ('2-3', '2pm - 3pm'),
        ('3-4', '3pm - 4pm')
    ], validators=[DataRequired()])
    
    venue = StringField("Venue", validators=[DataRequired(), Length(max=255)])
    prof_name = SelectField("Professional name", validators=[DataRequired()])
    service = SelectField("Service",  validators=[DataRequired()])
    submit = SubmitField("Add Appointment")
