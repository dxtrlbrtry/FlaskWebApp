from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[])
    picture = FileField('Post an Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    content = TextAreaField('Add Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
