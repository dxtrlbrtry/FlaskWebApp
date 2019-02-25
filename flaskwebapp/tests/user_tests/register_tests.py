from flaskwebapp.tests.TestBase import TestBase
from flask import url_for


class RegisterTestCases(TestBase):

    def test_go_to_register(self):
        self.client.get(url_for('users.register'))
        self.assertTemplateUsed('register.html')

    def test_go_to_register_while_logged_in(self):
        self.register('test_user', 'test@email.com', '123', '123')
        self.login('test@email.com', '123')

        self.client.get(url_for('users.register'))
        self.assertTemplateUsed('home.html')

    def test_register_successful(self):
        self.assert_redirects(
            self.register('test_user', 'test@email.com', '123', '123', False),
            url_for('users.login'))

    def test_register_existing_username(self):
        self.register('test_user', 'test@email.com', '123', '123')

        self.register('test_user', 'new_test@email.com', '123', '123')
        self.assertTemplateUsed('register.html')

    def test_register_empty_username(self):
        self.register('', 'test@email.com', '123', '123')
        self.assertTemplateUsed('register.html')

    def test_register_short_username(self):
        self.register('a', 'test@email.com', '123', '123')
        self.assertTemplateUsed('register.html')

    def test_register_long_username(self):
        self.register('test_user_test_user20', 'testemail.com', '123', '123')
        self.assertTemplateUsed('register.html')

    def test_register_existing_email(self):
        self.register('test_user', 'test@email.com', '123', '123')
        self.register('new_test_user', 'test@email.com', '123', '123')
        self.assertTemplateUsed('register.html')

    def test_register_empty_email(self):
        self.register('test_user', '', '123', '123')
        self.assertTemplateUsed('register.html')

    def test_register_invalid_email(self):
        self.register('test_user', 'testemail.com', '123', '123')
        self.assertTemplateUsed('register.html')

    def test_register_empty_password(self):
        self.register('test_user', 'test@email.com', '', '123')
        self.assertTemplateUsed('register.html')

    def test_register_empty_confirm_password(self):
        self.register('test_user', 'test@email.com', '123', '')
        self.assertTemplateUsed('register.html')

    def test_register_invalid_password_confirmation(self):
        self.register('test_user', 'test@email.com', '123', 'not_123')
        self.assertTemplateUsed('register.html')
