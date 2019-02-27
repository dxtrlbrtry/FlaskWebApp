from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import IntegerField, DateField, TimeField, DateTimeField, DateTimeLocalField


class EventForm(FlaskForm):
    theme = StringField('Theme', validators=[DataRequired()])
    start_date = DateTimeLocalField('Start Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    duration_hours = IntegerField('Hours', validators=[DataRequired()])
    duration_minutes = IntegerField('Minutes', validators=[DataRequired()])
    maximum_attendants = IntegerField('Max Slots', validators=[DataRequired()])
    location_name = StringField('Location', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Post')
