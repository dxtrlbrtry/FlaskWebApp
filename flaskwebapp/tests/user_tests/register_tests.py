from bs4 import BeautifulSoup
from flaskwebapp.tests.TestBase import TestBase
from flaskwebapp.tests.TestSteps import *


class RegisterTestCases(TestBase):
    def test_register_successful(self):
        response = register('test_user', 'test@email.com', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Your account has been created successfully!' \
               in soup.find('div', class_='alert').get_text()

    def test_register_existing_username(self):
        response = register('test_user', 'test@email.com', '123', '123')
        assert response.status_code == 200

        response = register('test_user', 'new_test@email.com', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'That username is taken. Choose a different one' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_empty_username(self):
        response = register('', 'test@email.com', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'This field is required' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_short_username(self):
        response = register('a', 'test@email.com', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Field must be between 2 and 20 characters long.' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_long_username(self):
        response = register('test_user_test_user20', 'testemail.com', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Field must be between 2 and 20 characters long.' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_existing_email(self):
        response = register('test_user', 'test@email.com', '123', '123')
        assert response.status_code == 200

        response = register('new_test_user', 'test@email.com', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'That email is taken. Choose a different one' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_empty_email(self):
        response = register('test_user', '', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'This field is required' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_invalid_email(self):
        response = register('test_user', 'testemail.com', '123', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Invalid email address.' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_empty_password(self):
        response = register('test_user', 'test@email.com', '', '123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'This field is required' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_empty_confirm_password(self):
        response = register('test_user', 'test@email.com', '123', '')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'This field is required' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_invalid_password_confirmation(self):
        response = register('test_user', 'test@email.com', '123', 'not_123')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Field must be equal to password.' \
               in soup.find('div', class_='invalid-feedback').get_text()

    def test_register_while_logged_in(self):
        response = register('test_user', 'test@email.com', '123', '123')
        assert response.status_code == 200

        response = login('test@email.com', '123')
        assert response.status_code == 200

        response = register('', '', '', '')
        soup = BeautifulSoup(response.data, 'html.parser')
        assert 'Join Today' not in soup.body.get_text()
