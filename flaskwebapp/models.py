from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskwebapp import db, login_manager
from flask_login import UserMixin
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


friend = db.Table('friend',
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                  db.Column('friend_id', db.Integer, db.ForeignKey('user.id')))

friend_requests = db.Table('friend_requests',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                           db.Column('friend_id', db.Integer, db.ForeignKey('user.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    access = db.Column(db.String(10), nullable=False, default='user')
    posts = db.relationship('Post', backref='author', lazy=True)
    requests = db.relationship('User',
                               secondary=friend_requests,
                               primaryjoin=(friend_requests.c.user_id == id),
                               secondaryjoin=(friend_requests.c.friend_id == id),
                               backref='request_of',
                               lazy='dynamic')
    friends = db.relationship('User',
                              secondary=friend,
                              primaryjoin=(friend.c.user_id == id),
                              secondaryjoin=(friend.c.friend_id == id),
                              backref='friend_of',
                              lazy='dynamic')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User(' {self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post(' {self.title}', '{self.date_posted}')"


class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    schedule = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"Sala(' {self.name}', '{self.address}')"
