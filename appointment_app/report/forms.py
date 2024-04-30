from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional

class AddReportForm(FlaskForm):
	feedback = TextAreaField('feedback', validators=[DataRequired()])
	submit = SubmitField('submit')