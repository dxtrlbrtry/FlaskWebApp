class Config:
    SECRET_KEY = 'd0ec579573c2f24c906a6d790c1d9b82'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'flaskzleitner@gmail.com'
    MAIL_PASSWORD = '#Arobs123'
