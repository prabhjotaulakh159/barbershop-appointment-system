from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField, FloatField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo


class AppointmentForm(FlaskForm):
    date_appointment = DateField(
        "Date", format='%Y-%m-%d', validators=[DataRequired()])
    slot = SelectField("Time Slot", validators=[DataRequired()])
    venue = StringField("Venue", validators=[DataRequired(), Length(max=255)])
    prof_name = SelectField("Professional name", validators=[DataRequired()])
    service = SelectField("Service",  validators=[DataRequired()])
    submit = SubmitField("Add Appointment")
