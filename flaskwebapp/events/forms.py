from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField, TimeField


class EventForm(FlaskForm):
    theme = StringField('Theme', validators=[DataRequired()])
    event_date = DateField('Event Date', format='%Y/%B/%d', validators=[DataRequired()])
    start_time = TimeField('Start Time', format='%H:%M', validators=[DataRequired()])
    duration = TimeField('Duration', format='%H:%M', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Post')
