########################################################
#
# this config file will be used to test the application
#
########################################################

import os

class test_Config:
    # Get top-level directory of the project
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # protect against modifying cookies and forgery attacks
    SECRET_KEY = 'verygoodsecretkey'

    # Set location of the database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'test_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # config for flask mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    # Enable the TESTING flag to disable the error catching during request handling
    # so that you get better error reports when performing test requests against the application.
    TESTING = True

    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False
