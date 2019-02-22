import os
import secrets
from PIL import Image
from flask import url_for, current_app, request, redirect, abort, flash
from flask_login import current_user
from flask_mail import Message
from flaskwebapp import mail
from functools import wraps


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics/', picture_fn)

    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn


def post_photo(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/posted_images/', picture_fn)

    output_size = (400, 300)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''
To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request, ignore this message
'''
    mail.send(msg)


def requires_access(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please login to access that page', 'info')
                return redirect(url_for('users.login'))
            if current_user.access != access_level:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
