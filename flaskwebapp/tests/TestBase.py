from unittest import TestCase
from flaskwebapp import create_app, db

app = create_app()
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests/test.db'
app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG'] = False


class TestBase(TestCase):
    def setUp(self):
        self.app = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

        response = self.app.get('/', follow_redirects=True)
        assert response.status_code == 200

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()


