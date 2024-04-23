from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField, FloatField,SelectField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo


class RegisterUserForm(FlaskForm):
    ''' class representing registration form '''
    username = StringField("Username", validators=[DataRequired(), Length(min=2,max=25)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Retype password", validators=[DataRequired(), EqualTo("password")])
    email = EmailField ('Email', validators=[DataRequired(),])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=10,max=12)])
    user_type = SelectField("Type", choices=[('Member', 'Member'), ('Professional', 'Professional')])
    age = FloatField(min=0,max=100)
    address = StringField("Address", validators=[DataRequired(), Length(min=2,max=25)])
    pay_rate = FloatField(min=1, max=100)
    specialty = SelectField("Specialty", choices=[
        ('Hair Stylist', 'Hair Stylist'),
        ('Colorist', 'Colorist'),
        ('Barber', 'Barber'),
        ('Other', 'Other')
    ])
    
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2,max=25)])
    email = EmailField('Email', validators=[DataRequired(), Length(min=2)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Login")