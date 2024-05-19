from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, date, timezone

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    User model class, inheriting from db.Model and UserMixin, used to represent the user table.
    """
    __tablename__ = 'user'  
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(80), unique=True, nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password_hash = db.Column(db.String(128))  
    likes = db.relationship('Like', backref='user', lazy=True)  
    comments = db.relationship('Comment', backref='user', lazy=True)  
    requests = db.relationship('Request', backref='author', lazy=True, overlaps="author,requests")  
    points = db.relationship('Point', back_populates='user', lazy='dynamic')  
    daily_activity = db.relationship('UserDailyActivity', back_populates='user', lazy='dynamic')  

    def set_password(self, password):
        """
        Set the user's password hash.

        Args:
        password (str): The plaintext password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the provided password matches the user's password hash.

        Args:
        password (str): The plaintext password

        Returns:
        bool: True if the passwords match, False otherwise
        """
        return check_password_hash(self.password_hash, password)

class Request(db.Model):
    """
    Request model class, used to represent the request table.
    """
    __tablename__ = 'requests'  
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(100), nullable=False)  
    description = db.Column(db.Text, nullable=False)  
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    likes = db.relationship('Like', backref='request', lazy=True)  
    comments = db.relationship('Comment', backref='request', lazy=True)  
    user = db.relationship('User', backref='user_requests', overlaps="author,requests")  

    def like_count(self):
        """
        Calculate the number of likes for the request.

        Returns:
        int: The number of likes
        """
        return len(self.likes)

class Like(db.Model):
    """
    Like model class, used to represent the like table.
    """
    __tablename__ = 'like'  
    id = db.Column(db.Integer, primary_key=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False)  

class Comment(db.Model):
    """
    Comment model class, used to represent the comment table.
    """
    __tablename__ = 'comment'  
    id = db.Column(db.Integer, primary_key=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False) 
    content = db.Column(db.Text, nullable=False)  
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))  

class Point(db.Model):
    """
    Point model class, used to represent the user's points table.
    """
    id = db.Column(db.Integer, primary_key=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    date = db.Column(db.Date, nullable=False)  
    points = db.Column(db.Integer, default=0)  
    type = db.Column(db.String(50), nullable=False)  
    user = db.relationship('User', back_populates='points') 

class UserDailyActivity(db.Model):
    """
    User daily activity model class, used to represent the table for recording user daily activities.
    """
    id = db.Column(db.Integer, primary_key=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    date = db.Column(db.Date, nullable=False, default=date.today)  
    likes_count = db.Column(db.Integer, default=0) 
    comments_count = db.Column(db.Integer, default=0)  
    user = db.relationship('User', back_populates='daily_activity') 
