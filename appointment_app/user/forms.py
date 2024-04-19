from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField, FloatField,SelectField
from wtforms.validators import DataRequired, Length, EqualTo


class RegisterClientForm(FlaskForm):
    ''' class representing a client registration form '''
    username = StringField("Username", validators=[DataRequired(), Length(min=2,max=25)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Retype password", validators=[DataRequired(), EqualTo("password")])
    email = EmailField ('Email', validators=[DataRequired(),])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=10,max=12)])
    submit=SubmitField("Register")

class RegisterProfessionalForm(RegisterClientForm):
    ''' class representing a professional registration form '''
    payrate = FloatField("Pay Rate", validators=[DataRequired()])
    specialty = SelectField("Specialty", choices=[
        ('hair_stylist', 'Hair Stylist'),
        ('colorist', 'Colorist'),
        ('barber', 'Barber'),
        ('other', 'Other')
    ])
    submit = SubmitField("Register")
    
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2,max=25)])
    email = EmailField ('Email', validators=[DataRequired(),])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
