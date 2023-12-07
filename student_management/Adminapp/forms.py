# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class StaffForm(FlaskForm):
    staff_name = StringField('Staff Name', validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired(), Length(min=10, max=10)])
    mail = StringField('Mail', validators=[DataRequired(), Length(max=250)])
    experience = StringField('Experience', validators=[DataRequired(), Length(max=250)])
    submit = SubmitField('Add Staff')
