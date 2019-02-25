from flaskwebapp import create_app, db, bcrypt
from flaskwebapp.models import User, Post, Event
from datetime import datetime

app = create_app()
app.app_context().push()


def create_all():
    with app.app_context():
        db.drop_all()
        db.create_all()

        db.session.commit()


def create_users():
    with app.app_context():
        user1 = User(username='dxtrlbrtry', password=bcrypt.generate_password_hash('123'), email='dxtrlbrtry@yahoo.com', access='admin')
        user2 = User(username='friend', password=bcrypt.generate_password_hash('123'), email='friend@yahoo.com')
        user3 = User(username='asd', password=bcrypt.generate_password_hash('123'), email='asd@asd.asd')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)

        db.session.commit()


def create_posts():
    with app.app_context():
        user1= User.query.filter_by(username='dxtrlbrtry').first()
        user2 = User.query.filter_by(username='asd').first()
        user3 = User.query.filter_by(username='friend').first()
        for x in range(1, 7):
            post1 = Post(title='title' + str(x), content='erwerqwerqwrqw' + str(x), author=user1)
            post2 = Post(title='title' + str(x), content='gdafgsdgas' + str(x), author=user2)
            post3 = Post(title='title' + str(x), content='gnmyutmmtut' + str(x), author=user3)
            db.session.add(post1)
            db.session.add(post2)
            db.session.add(post3)
        db.session.commit()


user1= User.query.filter_by(username='dxtrlbrtry').first()

event = Event(theme='sport', start_time=datetime.utcnow(), end_time=datetime.utcnow(), hosted_by=user1)
db.session.add(event)
db.session.commit()
print(event.hosted_by)
pass
