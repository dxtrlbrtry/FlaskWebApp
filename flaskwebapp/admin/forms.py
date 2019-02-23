from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    picture = FileField('Edit Profile Image', validators=[FileAllowed(['jpg', 'png'])])
    access = RadioField('Access level', choices=[('admin', 'admin access'), ('user', 'user access')])
    submit = SubmitField('Submit')


class AddFriend(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Add')
