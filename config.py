import os

class Config(object):
    # Secret key for the Flask application, used for session encryption and other security purposes
    SECRET_KEY = 'my_secret_key'

    # URI for the main SQLAlchemy database, pointing to the app.db file
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

    # Configuration for SQLAlchemy to bind to multiple databases, pointing to user.db and request.db files
    SQLALCHEMY_BINDS = {
        'users': 'sqlite:///user.db',        
        'requests': 'sqlite:///request.db'   
    }

    # Disable SQLAlchemy's modification tracking feature (can improve performance)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    # Use an in-memory SQLite database for the testing environment
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
