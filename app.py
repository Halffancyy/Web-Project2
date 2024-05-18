from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Request, Like, Comment, UserDailyActivity, Point
from forms import RegisterForm, LoginForm, RequestForm, CommentForm
from flask_migrate import Migrate
from datetime import date
from flask_apscheduler import APScheduler

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# 上下文处理器，为所有模板添加当前用户的积分
@app.context_processor
def inject_user_points():
    if current_user.is_authenticated:
        total_points = db.session.query(db.func.sum(Point.points)).filter(Point.user_id == current_user.id).scalar() or 0
        return {'user_points': total_points}
    return {}
    
# 默认介绍页面
@app.route('/')
def intro():
    return render_template('introductory.html')

# 用户注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('New user has been created!')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Error: ' + str(e), 'error')
            print('Error: ' + str(e))
    return render_template('register.html', form=form)

# 用户登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            # 添加积分逻辑
            today = date.today()
            if not Point.query.filter_by(user_id=user.id, date=today, type='login').first():
                point = Point(user_id=user.id, date=today, points=1, type='login')
                db.session.add(point)
                db.session.commit()
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

# 主页路由 (需要登录)
@app.route('/index')
@login_required
def index():
    # Query for the three most recent posts
    recent_posts = Request.query.order_by(Request.timestamp.desc()).limit(3).all()
    return render_template('index.html', recent_posts=recent_posts)


@app.route('/index-2')
@login_required
def index_2():
    return render_template('index-2.html')

# 画廊页面路由 (需要登录)
@app.route('/gallery')
@login_required
def gallery():
    return render_template('gallery.html')

@app.route('/post')
@login_required
def post():
    query = request.args.get('query')
    requests = Request.query.filter(
        Request.title.ilike(f'%{query}%') | Request.description.ilike(f'%{query}%')
    ).all() if query else Request.query.all()
    comment_form = CommentForm()
    # Get the new request's id from the query parameters
    new_request_id = request.args.get('request_id')
    return render_template('post.html', requests=requests, comment_form=comment_form, new_request_id=new_request_id)


# 单个帖子页面路由 (需要登录)
@app.route('/single-post')
@login_required
def single_post():
    return render_template('single-post.html')

# 单个帖子页面路由 (需要登录)
@app.route('/layout')
@login_required
def layout():
    return render_template('layout.html')


# 用户注销
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

# 仪表板页面，显示请求列表并允许用户进行搜索 (需要登录)
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    query = request.args.get('query')
    requests = Request.query.filter(
        Request.title.ilike(f'%{query}%') | Request.description.ilike(f'%{query}%')
    ).all() if query else Request.query.all()
    comment_form = CommentForm()
    return render_template('dashboard.html', requests=requests, comment_form=comment_form)

# 创建新请求的页面 (需要登录)(发帖)
@app.route('/create_request', methods=['GET', 'POST'])
@login_required
def create_request():
    form = RequestForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        new_request = Request(title=title, description=description, user_id=current_user.id)
        db.session.add(new_request)

        today = date.today()
        # 检查用户当天发帖是否已经获得积分5次
        points_today = Point.query.filter_by(user_id=current_user.id, date=today, type='post').count()
        if points_today < 5:
            # 添加积分
            point = Point(user_id=current_user.id, date=today, points=3, type='post')
            db.session.add(point)
            flash('+3 points for creating a post!', 'success')

        try:
            db.session.commit()
            flash('Request created successfully!', 'success')
            return redirect(url_for('post'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding request: {e}', 'error')
    
    return render_template('create_request.html', form=form)

# 点赞请求的接口 (需要登录)
@app.route('/like/<int:request_id>', methods=['POST'])
@login_required
def like_request(request_id):
    request = Request.query.get_or_404(request_id)
    today = date.today()
    
    # 获取用户当天的活动记录
    activity = UserDailyActivity.query.filter_by(user_id=current_user.id, date=today).first()
    if not activity:
        activity = UserDailyActivity(user_id=current_user.id, date=today, likes_count=0, comments_count=0)
        db.session.add(activity)
        db.session.commit()

    if not Like.query.filter_by(user_id=current_user.id, request_id=request_id).first():
        like = Like(user_id=current_user.id, request_id=request_id)
        db.session.add(like)
        if activity.likes_count < 5:
            print(f"Adding point, current likes count: {activity.likes_count}")
            point = Point(user_id=current_user.id, date=today, points=1, type='like')           
            db.session.add(point)
            flash('+1 point for liking!', 'success')
        activity.likes_count += 1
        db.session.add(activity)
        db.session.commit()
        return jsonify({'likes': request.like_count()})
    else:
        flash('Already liked', 'error')
        return jsonify({'error': 'Already liked'}), 400

# 评论请求的接口 (需要登录)
@app.route('/comment/<int:request_id>', methods=['POST'])
@login_required
def comment_request(request_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, request_id=request_id)
        today = date.today()

        # 获取用户当天的活动记录
        activity = UserDailyActivity.query.filter_by(user_id=current_user.id, date=today).first()
        if not activity:
            activity = UserDailyActivity(user_id=current_user.id, date=today, likes_count=0, comments_count=0)
            db.session.add(activity)
            db.session.commit()

        db.session.add(comment)
        if activity.comments_count < 10:
            points = 2 if len(form.content.data) > 50 else 1
            point = Point(user_id=current_user.id, date=today, points=points, type='comment')
            db.session.add(point)
            if points == 2:
                flash('+2 points for commenting!', 'success')
            else:
                flash('+1 point for commenting!', 'success')
        activity.comments_count += 1
        db.session.add(activity)
        db.session.commit()
        flash('Comment added successfully!', 'success')
    else:
        flash('Daily comment limit reached', 'error')
    return redirect(url_for('dashboard'))

# 积分排行榜
@app.route('/leaderboard')
@login_required
def leaderboard():
    scores = db.session.query(
        User.username,
        db.func.sum(Point.points).label('total_points')
    ).join(Point).group_by(User.id).order_by(db.desc('total_points')).all()
    return render_template('index.html', scores=scores, enumerate=enumerate)

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

# 初始化和启动调度器
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
scheduler.add_job(id='Reset Daily Activity', func=reset_daily_activity, trigger='cron', hour=0)

if __name__ == '__main__':
    app.run(debug=True)
