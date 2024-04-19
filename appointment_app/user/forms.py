from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class RegisterClientForm(FlaskForm):
    ''' class representing a client registration form '''
    username = StringField("Username", validators=[DataRequired(), Length(min=2,max=25)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Retype password", validators=[DataRequired(), EqualTo("password")])
    email = EmailField ('Email', validators=[DataRequired(),])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=10,max=12)])
    submit = SubmitField("Register")
    
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2,max=25)])
    email = EmailField ('Email', validators=[DataRequired(),])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
