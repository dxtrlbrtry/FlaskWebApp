from flask import Blueprint, request, render_template, flash, redirect, url_for
from flaskwebapp import db
from flaskwebapp.users.utils import requires_access
from flaskwebapp.models import User, Post
from flaskwebapp.admin.forms import EditUserForm, AddFriend

admin = Blueprint('admin', __name__)


@admin.route('/admin/')
@requires_access('admin')
def control_panel():
    users = User.query.all()
    return render_template('control_panel.html', users=users)


@admin.route('/admin/<string:username>/', methods=['GET', 'POST'])
@requires_access('admin')
def edit_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EditUserForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.access = form.access.data
        db.session.commit()
        flash(f'User updated', 'success')
        return redirect(url_for('admin.edit_user', username=user.username))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.image_file.data = user.image_file
        form.access.data = user.access
    return render_template('edit_user.html', user=user, form=form)


@admin.route('/admin/<string:username>/friends/', methods=['GET', 'POST'])
@requires_access('admin')
def edit_friends(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = AddFriend()
    if form.validate_on_submit():
        user_to_add = User.query.filter_by(username=form.username.data).first_or_404()
        if user_to_add in user.friends:
            flash(f'User already in friends list', 'warning')
            return redirect(url_for('admin.edit_friends', username=username))
        user.friends.append(user_to_add)
        user_to_add.friends.append(user)
        db.session.commit()
        flash(f'{user_to_add.username} and {user.username} are now friends', 'success')
        return redirect(url_for('admin.edit_friends', username=username))
    return render_template('edit_friends.html', user=user, form=form)


@admin.route('/admin/user/<string:username>/remove/<string:target_user>', methods=['GET'])
@requires_access('admin')
def remove_friend(username, target_user):
    user = User.query.filter_by(username=username).first_or_404()
    user_to_delete = User.query.filter_by(username=target_user).first_or_404()
    if user_to_delete not in user.friends:
        flash('Cannot unfriend, you are not friends yet', 'warning')
    else:
        user.friends.remove(user_to_delete)
        user_to_delete.friends.remove(user)
        db.session.commit()
        flash(f'You successfully unfriended ' + user.username + '.', 'success')
    return redirect(url_for('admin.edit_friends', username=user.username))


@admin.route('/admin/user/<string:username>/delete/', methods=['GET'])
@requires_access('admin')
def delete_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    for post in user.posts:
        db.session.delete(post)
    for request in user.requests:
        db.session.delete(request)
    for friend in user.friends:
        friend.friends.remove(user)
    db.session.delete(user)
    db.session.commit()
    flash(f'You successfully deleted ' + user.username + '.', 'success')
    return redirect(url_for('admin.control_panel', username=user.username))
