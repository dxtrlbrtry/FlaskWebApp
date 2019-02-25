from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flaskwebapp import db, bcrypt
from flaskwebapp.models import User
from flaskwebapp.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordForm, RequestResetForm
from flaskwebapp.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created successfully!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form, friends=current_user.friends)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(f'An email has been set with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated. You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route('/user/<string:username>/remove/', methods=['GET'])
@login_required
def remove_friend(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user not in current_user.friends:
        flash('Cannot unfriend, you are not friends yet', 'warning')
    else:
        current_user.friends.remove(user)
        user.friends.remove(current_user)
        db.session.commit()
        flash(f'You successfully unfriended ' + user.username + '.', 'success')
    return redirect(url_for('posts.user_posts', username=username))


@users.route('/user/<string:username>/send/', methods=['GET'])
@login_required
def send_request(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user == current_user:
        abort(403)
    if current_user in user.requests:
        flash(f'Friend request already sent but is still pending', 'warning')
        return redirect(url_for('users.user_posts', username=user.username))
    if user in current_user.friends:
        flash(f'User already in friendslist', 'warning')
        return redirect(url_for('users.user_posts', username=user.username))
    if user in current_user.requests:
        flash(f'You already have a request from that user', 'warning')
        return redirect(url_for('users.user_posts', username=user.username))
    else:
        user.requests.append(current_user)
        db.session.commit()
        flash(f'Friend request sent to ' + user.username + '.', 'success')
    return redirect(url_for('posts.user_posts', username=user.username))


@users.route('/requests/', methods=['GET'])
@login_required
def requests():
    return render_template('requests.html', requests=current_user.requests)


@users.route('/requests/<string:username>/accept/', methods=['POST'])
@login_required
def accept_request(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user in current_user.friends:
        current_user.requests.remove(user)
        flash('You are already friends', 'warning')
    else:
        current_user.requests.remove(user)
        current_user.friends.append(user)
        user.friends.append(current_user)
        db.session.commit()
        flash(f'You added ' + user.username + ' to your friends list', 'success')
    return redirect(url_for('users.requests', username=username))


@users.route('/request/<string:username>/refuse', methods=['POST'])
@login_required
def refuse_request(username):
    user = User.query.filter_by(username=username).first_or_404()
    current_user.requests.remove(user)
    db.session.commit()
    flash(f'Friend request deleted', 'info')
    return redirect(url_for('users.requests', username=username))
