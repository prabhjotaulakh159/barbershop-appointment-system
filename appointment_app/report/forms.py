from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Optional, Length

class AddReportForm(FlaskForm):
	feedback_client = TextAreaField('feedback client', validators=[Length(min=2, max=255)])
	feedback_professional = TextAreaField('feedback professional', validators=[Optional(), Length(min=2, max=255)])
	submit = SubmitField('submit')