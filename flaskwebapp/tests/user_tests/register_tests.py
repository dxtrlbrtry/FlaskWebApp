from bs4 import BeautifulSoup
from flaskwebapp.tests.TestBase import TestBase
from flask import url_for


class RegisterTestCases(TestBase):
    def test_register_successful(self):
        response = self.register('test_user', 'test@email.com', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Your account has been created successfully!' \
               in soup.find('div', class_='alert').get_text()

        response = self.client.get('/')
        self.assert_redirects(response, url_for('users.login'))

    def test_register_existing_username(self):
        response = self.register('test_user', 'test@email.com', '123', '123')
        assert response.status_code == 200

        response = self.register('test_user', 'new_test@email.com', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'That username is taken. Choose a different one' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_empty_username(self):
        response = self.register('', 'test@email.com', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'This field is required' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_short_username(self):
        response = self.register('a', 'test@email.com', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Field must be between 2 and 20 characters long.' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_long_username(self):
        response = self.register('test_user_test_user20', 'testemail.com', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Field must be between 2 and 20 characters long.' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_existing_email(self):
        response = self.register('test_user', 'test@email.com', '123', '123')
        assert response.status_code == 200

        response = self.register('new_test_user', 'test@email.com', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'That email is taken. Choose a different one' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_empty_email(self):
        response = self.register('test_user', '', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'This field is required' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_invalid_email(self):
        response = self.register('test_user', 'testemail.com', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Invalid email address.' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_empty_password(self):
        response = self.register('test_user', 'test@email.com', '', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'This field is required' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_empty_confirm_password(self):
        response = self.register('test_user', 'test@email.com', '123', '')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'This field is required' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_invalid_password_confirmation(self):
        response = self.register('test_user', 'test@email.com', '123', 'not_123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Field must be equal to password.' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_while_logged_in(self):
        self.client.get(url_for('users.register'))
        self.assertTemplateUsed('register.html')

        response = self.register('test_user', 'test@email.com', '123', '123')
        assert response.status_code == 200

        response = self.login('test@email.com', '123')
        assert response.status_code == 200

        self.render_templates = False

        self.client.get(url_for('users.register'))
        self.assertTemplateUsed('home.html')
