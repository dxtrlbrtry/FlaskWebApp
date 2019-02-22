from bs4 import BeautifulSoup
from flaskwebapp.tests.TestBase import TestBase
from flaskwebapp.tests.TestSteps import *


class LoginTestCases(TestBase):
    def test_login_successful(self):
        response = register('test_user', 'test@email.com', '123', '123')
        assert response.status_code == 200

        response = login('test@email.com', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Hello test_user' in soup.body.get_text()

    def test_login_with_empty_email(self):
        response = login('', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'This field is required' in soup.body.get_text()

    def test_login_with_inexistent_email(self):
        response = login('not_test@email.com', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Invalid username or password' in soup.body.get_text()

    def test_login_with_invalid_email(self):
        response = login('testemail.com', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Invalid email address.' in soup.body.get_text()

    def test_login_with_empty_password(self):
        response = login('test@email.com', '')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'This field is required' in soup.body.get_text()

    def test_login_with_wrong_password(self):
        response = login('test@email.com', 'not_123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Invalid username or password' in soup.body.get_text()

    def test_login_while_logged_in(self):
        response = register('test_user', 'test@email.com', '123', '123')
        assert response.status_code == 200

        response = login('test@email.com', '123')
        assert response.status_code == 200

        response = login('', '')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Log In' not in soup.body.get_text()

    def test_logout(self):
        response = register('test_user', 'test@email.com', '123', '123')
        assert response.status_code == 200

        response = login('test@email.com', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Hello test_user' in soup.body.get_text()

        response = logout()
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Hello test_user' not in soup.body.get_text()
