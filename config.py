import os

class Config(object):
    SECRET_KEY = os.urandom(24)  # Used for encrypting sessions
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
