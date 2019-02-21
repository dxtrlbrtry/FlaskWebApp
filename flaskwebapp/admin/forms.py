from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    image_file = StringField('Image file', validators=[DataRequired()])
    access = RadioField('Access level', choices=[('admin', 'admin access'), ('user', 'user access')])
    submit = SubmitField('Submit')


class AddFriend(FlaskForm):
    username = username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Add')
