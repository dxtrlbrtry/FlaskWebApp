from bs4 import BeautifulSoup
from flaskwebapp.tests.TestBase import TestBase
from flask import url_for


class LoginTestCases(TestBase):
    def test_go_to_login(self):
        self.register('test_user', 'test@email.com', '123', '123')
        self.assertRedirects(
            self.login('test@email.com', '123', False),
            url_for('main.home'))

    def test_go_to_login_while_logged_in(self):
        self.register('test_user', 'test@email.com', '123', '123')
        self.login('test@email.com', '123')
        self.assertRedirects(
            self.client.get(url_for('users.login')),
            url_for('main.home'))

    def test_login_successful(self):
        response = self.register('test_user', 'test@email.com', '123', '123')
        assert response.status_code == 200

        response = self.login('test@email.com', '123')
        soup = BeautifulSoup(response.data, 'html.parser')#
        assert 'Hello test_user' in soup.body.get_text()

    def test_login_with_empty_email(self):
        response = self.login('', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'This field is required' in soup.body.get_text()

    def test_login_with_inexistent_email(self):
        response = self.login('not_test@email.com', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Invalid username or password' in soup.body.get_text()

    def test_login_with_invalid_email(self):
        response = self.login('testemail.com', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Invalid email address.' in soup.body.get_text()

    def test_login_with_empty_password(self):
        response = self.login('test@email.com', '')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'This field is required' in soup.body.get_text()

    def test_login_with_wrong_password(self):
        response = self.login('test@email.com', 'not_123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Invalid username or password' in soup.body.get_text()

    def test_login_while_logged_in(self):
        response = self.register('test_user', 'test@email.com', '123', '123')
        assert response.status_code == 200

        response = self.login('test@email.com', '123')
        assert response.status_code == 200

        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Log In' not in soup.body.get_text()

    def test_logout(self):
        response = self.register('test_user', 'test@email.com', '123', '123')
        assert response.status_code == 200

        response = self.login('test@email.com', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Hello test_user' in soup.body.get_text()

        response = self.logout()
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Hello test_user' not in soup.body.get_text()
