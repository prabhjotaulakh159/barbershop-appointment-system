<<<<<<< HEAD
''' Forms for reports '''
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class AddReportForm(FlaskForm):
    ''' Form to add a report '''
=======

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class AddReportForm(FlaskForm):
    '''class representing a report form'''
>>>>>>> 35f76ac2080bc4d090c254ce5f9ee5b756d7e8d4
    feedback = TextAreaField('feedback', validators=[DataRequired()])
    submit = SubmitField('submit')
