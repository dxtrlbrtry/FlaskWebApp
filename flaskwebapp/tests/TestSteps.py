class TestSteps:
    app = set()

    def __init__(self, test_app):
        self.app = test_app

    def register(self, username='', email='', password='', confirm_password='', method='GET', follow_redirects=False):
        if method is 'GET':
            return self.app.client.get('/register/', follow_redirects=follow_redirects)
        if method is 'POST':
            return self.app.client.post('/register/', data=dict(
                username=username,
                email=email,
                password=password,
                confirm_password=confirm_password
            ))

    def login(self, email, password, method='GET', follow_redirects=True):

        return self.app.client.post('/login/', data=dict(
            email=email,
            password=password
        ), follow_redirects=follow_redirects)

    def logout(self, method='GET'):
        return self.app.client.get('/logout/', follow_redirects=True)


