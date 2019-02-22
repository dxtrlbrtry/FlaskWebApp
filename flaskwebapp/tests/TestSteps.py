from flaskwebapp.tests.TestBase import app
app = app.test_client()


def register(username, email, password, confirm_password):
    return app.post('/register/', data=dict(
        username=username,
        email=email,
        password=password,
        confirm_password=confirm_password),
                         follow_redirects=True)


def login(email, password):
    return app.post('/login/', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout():
    return app.get('/logout/', follow_redirects=True)
