from flask_testing import TestCase
from flaskwebapp import create_app, db


class TestBase(TestCase):

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tests/test.db'
    SECRET_KEY = 'secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    DEBUG = False
    render_templates = False

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register(self, username, email, password, confirm_password, follow_redirects=True):
        return self.client.post('/register/', data=dict(
            username=username,
            email=email,
            password=password,
            confirm_password=confirm_password),
                        follow_redirects=follow_redirects)

    def login(self, email, password, follow_redirects=True):
        return self.client.post('/login/', data=dict(
            email=email,
            password=password
        ), follow_redirects=follow_redirects)

    def logout(self):
        return self.client.get('/logout/', follow_redirects=True)


