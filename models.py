from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, date, timezone

# 初始化 SQLAlchemy
db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    用户模型类，继承自 db.Model 和 UserMixin，用于表示用户表。
    """
    __tablename__ = 'user'  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 用户ID，主键
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名，唯一且不能为空
    email = db.Column(db.String(120), unique=True, nullable=False)  # 邮箱，唯一且不能为空
    password_hash = db.Column(db.String(128))  # 密码哈希
    likes = db.relationship('Like', backref='user', lazy=True)  # 与 Like 模型的关系，一对多
    comments = db.relationship('Comment', backref='user', lazy=True)  # 与 Comment 模型的关系，一对多
    requests = db.relationship('Request', backref='author', lazy=True, overlaps="author,requests")  # 与 Request 模型的关系，一对多
    points = db.relationship('Point', back_populates='user', lazy='dynamic')  # 与 Point 模型的关系，一对多
    daily_activity = db.relationship('UserDailyActivity', back_populates='user', lazy='dynamic')  # 与 UserDailyActivity 模型的关系，一对多

    def set_password(self, password):
        """
        设置用户密码哈希值。
        
        参数:
        password (str): 明文密码
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        检查用户密码是否匹配。
        
        参数:
        password (str): 明文密码
        
        返回:
        bool: 如果密码匹配则返回 True，否则返回 False
        """
        return check_password_hash(self.password_hash, password)

class Request(db.Model):
    """
    请求模型类，用于表示请求表。
    """
    __tablename__ = 'requests'  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 请求ID，主键
    title = db.Column(db.String(100), nullable=False)  # 请求标题，不能为空
    description = db.Column(db.Text, nullable=False)  # 请求描述，不能为空
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)  # 时间戳，默认为当前时间，不能为空
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 用户ID，外键，不能为空
    likes = db.relationship('Like', backref='request', lazy=True)  # 与 Like 模型的关系，一对多
    comments = db.relationship('Comment', backref='request', lazy=True)  # 与 Comment 模型的关系，一对多
    user = db.relationship('User', backref='user_requests', overlaps="author,requests")  # 与 User 模型的关系，多对一

    def like_count(self):
        """
        计算点赞数。
        
        返回:
        int: 点赞数
        """
        return len(self.likes)

class Like(db.Model):
    """
    点赞模型类，用于表示点赞表。
    """
    __tablename__ = 'like'  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 点赞ID，主键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 用户ID，外键，不能为空
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False)  # 请求ID，外键，不能为空

class Comment(db.Model):
    """
    评论模型类，用于表示评论表。
    """
    __tablename__ = 'comment'  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 评论ID，主键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 用户ID，外键，不能为空
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False)  # 请求ID，外键，不能为空
    content = db.Column(db.Text, nullable=False)  # 评论内容，不能为空
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))  # 时间戳，默认为当前时间，不能为空

class Point(db.Model):
    """
    积分模型类，用于表示用户积分表。
    """
    id = db.Column(db.Integer, primary_key=True)  # 积分ID，主键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 用户ID，外键，不能为空
    date = db.Column(db.Date, nullable=False)  # 日期，不能为空
    points = db.Column(db.Integer, default=0)  # 积分，默认为0
    type = db.Column(db.String(50), nullable=False)  # 积分类型，例如 'login', 'like', 'comment', 'time_spent' 等

    user = db.relationship('User', back_populates='points')  # 与 User 模型的关系，多对一

class UserDailyActivity(db.Model):
    """
    用户每日活动模型类，用于表示用户每日活动记录表。
    """
    id = db.Column(db.Integer, primary_key=True)  # 活动ID，主键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 用户ID，外键，不能为空
    date = db.Column(db.Date, nullable=False, default=date.today)  # 日期，默认为今天，不能为空
    likes_count = db.Column(db.Integer, default=0)  # 点赞数，默认为0
    comments_count = db.Column(db.Integer, default=0)  # 评论数，默认为0

    user = db.relationship('User', back_populates='daily_activity')  # 与 User 模型的关系，多对一
