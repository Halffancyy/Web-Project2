import os

class Config(object):
    # Flask 应用的密钥，用于加密 session 和其他安全用途
    SECRET_KEY = 'my_secret_key'

    # SQLAlchemy 主数据库的 URI，指向 app.db 文件
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

    # SQLAlchemy 多绑定数据库的配置，分别指向 user.db 和 request.db 文件
    SQLALCHEMY_BINDS = {
        'users': 'sqlite:///user.db',        # 绑定 'users' 数据库，存储用户数据
        'requests': 'sqlite:///request.db'   # 绑定 'requests' 数据库，存储请求数据
    }

    # 禁用 SQLAlchemy 的修改追踪功能（可以提高性能）
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    # 使用内存中的 SQLite 数据库用于测试环境
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
