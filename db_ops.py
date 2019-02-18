from flaskwebapp import create_app, db, bcrypt
from flaskwebapp.models import User, Post, Sala

app = create_app()
app.app_context().push()

user1 = User(username='dxtrlbrtry', password=bcrypt.generate_password_hash('123'), email='dxtrlbrtry@yahoo.com')
user2 = User(username='friend', password=bcrypt.generate_password_hash('123'), email='friend@yahoo.com')
user3 = User(username='asd', password=bcrypt.generate_password_hash('123'), email='asd@asd.asd')


def create_all():
    with app.app_context():
        db.drop_all()
        db.create_all()

        db.session.add(user1)

        db.session.commit()


def create_users():
    with app.app_context():
        db.session.add(user2)
        db.session.add(user3)

        db.session.commit()


create_all()
create_users()
print(User.query.all())
print(Post.query.all())
