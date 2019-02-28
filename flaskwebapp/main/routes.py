from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from flaskwebapp.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home/')
def home():
    if current_user.is_authenticated:
        posts = Post.query.order_by(Post.date_posted.desc())
        return render_template('home.html', posts=posts)
    return redirect(url_for('users.login'))


@main.route('/about/')
def about():
    return render_template('about.html', title='About')


@main.route('/test/')
def test():
    return render_template('test.html')

