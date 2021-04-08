import os

class Config:
    # protect against modifying cookies and forgery attacks
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Set location of the database
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # config for flask mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # API
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY')