from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Request, Like, Comment
from forms import RegisterForm, LoginForm, RequestForm, CommentForm

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
db.init_app(app)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

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
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

# 主页路由 (需要登录)
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

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
    return render_template('post.html', requests=requests, comment_form=comment_form)

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

# 创建新请求的页面 (需要登录)
@app.route('/create_request', methods=['GET', 'POST'])
@login_required
def create_request():
    form = RequestForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        new_request = Request(title=title, description=description)
        try:
            db.session.add(new_request)
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
    if not Like.query.filter_by(user_id=current_user.id, request_id=request_id).first():
        like = Like(user_id=current_user.id, request_id=request_id)
        db.session.add(like)
        db.session.commit()
        return jsonify({'likes': request.like_count()})
    else:
        return jsonify({'error': 'Already liked'}), 400

# 评论请求的接口 (需要登录)
@app.route('/comment/<int:request_id>', methods=['POST'])
@login_required
def comment_request(request_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, request_id=request_id)
        try:
            db.session.add(comment)
            db.session.commit()
            flash('Comment added successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding comment: {e}', 'error')
    return redirect(url_for('dashboard'))

# 处理 404 错误
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# 处理 500 错误
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
