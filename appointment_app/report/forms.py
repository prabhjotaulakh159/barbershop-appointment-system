from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class AddReportForm(FlaskForm):
	feedback_client = TextAreaField('feedback client', validators=[DataRequired(), Length(min=2, max=255)])
	feedback_professional = TextAreaField('feedback professional', validators=[DataRequired(), Length(min=2, max=255)])
	submit = SubmitField('submit')