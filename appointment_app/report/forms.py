
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class AddReportForm(FlaskForm):
    '''class representing a report form'''
    feedback = TextAreaField('feedback', validators=[DataRequired()])
    submit = SubmitField('submit')
