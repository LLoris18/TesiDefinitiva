import secrets
from flask_sqlalchemy import SQLAlchemy
import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = secrets.token_hex(32)
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/Database'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Aggiunto per evitare un warning
    UPLOADS = "/home/username/app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = True
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = '07e8d2df12b27d'
    MAIL_PASSWORD = '26dbf278d1a525'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    DB_NAME = "testing-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"
