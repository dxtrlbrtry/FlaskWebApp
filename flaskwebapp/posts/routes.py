from flask_login import login_required, current_user
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flaskwebapp import db
from flaskwebapp.models import Post
from flaskwebapp.posts.forms import PostForm
from flaskwebapp.users.utils import post_photo

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    author=current_user)
        if form.content.data:
            post.content = form.content.data
        if form.picture.data:
            picture_file = post_photo(form.picture.data)
            post.image_file = picture_file
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form)


@posts.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, legend='New Post', post=post)


@posts.route('/post/<int:post_id>/update/', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', legend='Update Post', form=form)


@posts.route('/post/<int:post_id>/delete/', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route('/post/<int:post_id>/like/', methods=['GET'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user not in post.liked_by:
        post.liked_by.append(current_user)
    else:
        post.liked_by.remove(current_user)
    db.session.commit()
    return redirect(url_for('main.home'))
