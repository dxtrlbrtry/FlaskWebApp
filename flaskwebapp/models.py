from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskwebapp import db, login_manager
from flask_login import UserMixin
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


likes = db.Table('likes',
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                  db.Column('post_id', db.Integer, db.ForeignKey('post.id')))

friend = db.Table('friend',
                  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                  db.Column('friend_id', db.Integer, db.ForeignKey('user.id')))

friend_requests = db.Table('friend_requests',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                           db.Column('friend_id', db.Integer, db.ForeignKey('user.id')))

event_requests = db.Table('event_requests',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                           db.Column('event_id', db.Integer, db.ForeignKey('event.id')))

event_attendants = db.Table('event_attendants',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                           db.Column('event_id', db.Integer, db.ForeignKey('event.id')))

event_invites = db.Table('event_invites',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                           db.Column('event_id', db.Integer, db.ForeignKey('event.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    access = db.Column(db.String(10), nullable=False, default='user')

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    likes = db.relationship('Post', secondary=likes, backref='liked_by', lazy='dynamic')

    hosted_events = db.relationship('Event', backref='host', lazy='dynamic')
    attended_events = db.relationship('Event', secondary=event_attendants, lazy='subquery', backref=db.backref('attendants', lazy=True))
    invites = db.relationship('Event', secondary=event_invites, lazy='subquery', backref=db.backref('invites_sent', lazy=True))

    requests = db.relationship('User', secondary=friend_requests,
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
    content = db.Column(db.Text, nullable=True)
    image_file = db.Column(db.String(20), nullable=True)

    comments = db.relationship('Comment', backref='comment_on', lazy='dynamic')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post(' {self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maximum_attendants = db.Column(db.Integer, nullable=False)
    theme = db.Column(db.String(100), nullable=False)
    location_name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    host_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    join_requests = db.relationship('User', secondary=event_requests, backref='requester', lazy=False, uselist=True)

    def __repr__(self):
        return f"Event(' {self.host}', '{self.theme}')"
