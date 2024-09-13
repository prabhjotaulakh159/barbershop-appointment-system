''' Contains form used by super admin '''
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import EmailField, PasswordField, StringField, SubmitField, SelectField, FileField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Regexp, Optional
from appointment_app.user.forms import PHONE_REGEX


class AdminCrudForm(FlaskForm):
    ''' Form to create and update new admins '''    
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=25)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Retype password", validators=[DataRequired(), EqualTo("password")])
    email = EmailField('Email', validators=[DataRequired()])
    phone = StringField("Phone", validators=[DataRequired(), Regexp(PHONE_REGEX, message='Phone number not valid')])
    user_type = SelectField("Type", choices=[('Admin User', 'Admin User'), ('Admin Appointment', 'Admin appointment')])
    age = IntegerField(validators=[NumberRange(min=0, max=100)])
    address = StringField("Address", validators=[DataRequired(), Length(min=2, max=25)])
    avatar = FileField('Avatar', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Register")