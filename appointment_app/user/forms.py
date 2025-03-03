'''Contains forms for authentication'''

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from wtforms import EmailField, PasswordField, StringField, SubmitField, SelectField, FileField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Regexp, Optional


PHONE_REGEX = '^[0-9]{3,3}-[0-9]{3,3}-[0-9]{4,4}$'


class RegisterUserForm(FlaskForm):
    '''Class representing registration form'''
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=25)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Retype password", validators=[DataRequired(), EqualTo("password")])
    email = EmailField('Email', validators=[DataRequired()])
    phone = StringField("Phone", validators=[DataRequired(), Regexp(PHONE_REGEX, message='Phone number not valid')])
    user_type = SelectField("Type", choices=[('Member', 'Member'), ('Professional', 'Professional')])
    age = IntegerField(validators=[NumberRange(min=0, max=100)])
    address = StringField("Address", validators=[DataRequired(), Length(min=2, max=25)])
    pay_rate = FloatField(validators=[Optional(), NumberRange(min=1, max=100)])
    avatar = FileField('Avatar', validators=[FileAllowed(['jpg', 'png'])])
    specialty = SelectField("Specialty", choices=[('Hair Stylist', 'Hair Stylist'), ('Colorist', 'Colorist'), ('Barber', 'Barber'), ('Other', 'Other')])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    '''Form for login'''
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=25)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=2)])
    submit = SubmitField("Login")


class ChangePasswordForm(FlaskForm):
    '''Form to change passwords'''
    old_password = PasswordField("Old Password", validators=[DataRequired(), Length(min=5)])
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=5)])
    confirm_new_password = PasswordField("Confirm New Password", validators=[DataRequired(), Length(min=5), EqualTo("new_password")])
    submit = SubmitField("Change Password")
