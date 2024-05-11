import os

class Config(object):
    SECRET_KEY = 'my_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///user.db'
    SQLALCHEMY_BINDS = {
        'users':        'sqlite:///user.db',
        'requests':     'sqlite:///request.db'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
