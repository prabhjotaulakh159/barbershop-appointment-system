''' Forms for reports '''
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class AddReportForm(FlaskForm):
    ''' Form to add a report '''
    feedback = TextAreaField('feedback', validators=[DataRequired()])
    submit = SubmitField('submit')
