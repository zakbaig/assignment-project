import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_EMAIL_ADDRESS = os.environ.get('ADMIN_EMAIL_ADDRESS')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = False
    USER_REQUIRE_RETYPE_PASSWORD = False