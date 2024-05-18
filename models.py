from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, date
from flask_migrate import Migrate

# 初始化 SQLAlchemy
db = SQLAlchemy()

# 用户模型，继承自 db.Model 和 UserMixin
class User(db.Model, UserMixin):
    __tablename__ = 'user'  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 用户ID，主键
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名，唯一且不能为空
    email = db.Column(db.String(120), unique=True, nullable=False)  # 邮箱，唯一且不能为空
    password_hash = db.Column(db.String(128))  # 密码哈希
    likes = db.relationship('Like', backref='user', lazy=True)  # 与 Like 模型的关系，一对多
    comments = db.relationship('Comment', backref='user', lazy=True)  # 与 Comment 模型的关系，一对多
    requests = db.relationship('Request', backref='author', lazy=True)
    points = db.relationship('Point', back_populates='user', lazy='dynamic')
    daily_activity = db.relationship('UserDailyActivity', back_populates='user', lazy='dynamic')

    # 设置密码哈希
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检查密码是否匹配
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 请求模型，继承自 db.Model
class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('Like', backref='request', lazy=True)
    comments = db.relationship('Comment', backref='request', lazy=True)
    user = db.relationship('User', backref='user_requests')

    # 计算点赞数
    def like_count(self):
        return len(self.likes)

# 点赞模型，继承自 db.Model
class Like(db.Model):
    __tablename__ = 'like'  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 点赞ID，主键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键，关联用户
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False)  # 外键，关联请求

# 评论模型，继承自 db.Model
class Comment(db.Model):
    __tablename__ = 'comment'  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 评论ID，主键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键，关联用户
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=False)  # 外键，关联请求
    content = db.Column(db.Text, nullable=False)  # 评论内容，不能为空
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # 时间戳，默认为当前时间

# 积分
class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    points = db.Column(db.Integer, default=0)
    type = db.Column(db.String(50), nullable=False)  # 如 'login', 'like', 'comment', 'time_spent'

    user = db.relationship('User', back_populates='points')

class UserDailyActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)

    user = db.relationship('User', back_populates='daily_activity')

