from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Request, Like, Comment, UserDailyActivity, Point
from flask_migrate import Migrate
from datetime import date
from flask_apscheduler import APScheduler

# Blueprints
from auth import auth as auth_blueprint
from posts import posts as posts_blueprint
from comments import comments as comments_blueprint
from site_views import site_views as site_blueprint

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf = CSRFProtect(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(posts_blueprint, url_prefix='/posts')
    app.register_blueprint(comments_blueprint, url_prefix='/comments')
    app.register_blueprint(site_blueprint, url_prefix='')

    with app.app_context():
        db.create_all()

    # 上下文处理器，为所有模板添加当前用户的积分
    @app.context_processor
    def inject_user_points():
        if current_user.is_authenticated:
            total_points = db.session.query(db.func.sum(Point.points)).filter(Point.user_id == current_user.id).scalar() or 0
            return {'user_points': total_points}
        return {}

    # 要删的
    # 单个帖子页面路由 (需要登录)
    @app.route('/layout')
    @login_required
    def layout():
        return render_template('layout.html')

    # 处理 404 错误
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # 处理 500 错误
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    # 定时任务：每日重置用户活动
    def reset_daily_activity():
        today = date.today()
        # 删除旧的记录或者重置计数
        UserDailyActivity.query.filter(UserDailyActivity.date < today).delete()
        db.session.commit()

    # APScheduler
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='Reset Daily Activity', func=reset_daily_activity, trigger='cron', hour=0)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
