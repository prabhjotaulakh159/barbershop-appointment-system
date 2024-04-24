from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import EmailField, PasswordField, StringField, SubmitField, FloatField,SelectField, FloatField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Optional


class RegisterUserForm(FlaskForm):
    ''' class representing registration form '''
    username = StringField("Username", validators=[DataRequired(), Length(min=2,max=25)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Retype password", validators=[DataRequired(), EqualTo("password")])
    email = EmailField ('Email', validators=[DataRequired(),])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=10,max=12)])
    user_type = SelectField("Type", choices=[('Member', 'Member'), ('Professional', 'Professional')])
    age = FloatField(validators=[NumberRange(min=0, max=100)])
    address = StringField("Address", validators=[DataRequired(), Length(min=2,max=25)])
    pay_rate = FloatField(validators=[Optional(),NumberRange(min=1, max=100)])
    avatar = FileField('avatar', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    specialty = SelectField("Specialty", choices=[
        ('Hair Stylist', 'Hair Stylist'),
        ('Colorist', 'Colorist'),
        ('Barber', 'Barber'),
        ('Other', 'Other')
    ])
    
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2,max=25)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Login")