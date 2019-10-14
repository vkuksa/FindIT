import os


class Config:
    SECRET_KEY = '5d26021b-58b7-4fab-adcb-343bfdfcdc12'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///storage.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
