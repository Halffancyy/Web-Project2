from . import site_views
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, User, Request, Like, Comment, Point
from comments.forms import CommentForm
from datetime import date

# 默认介绍页面
@site_views.route('/')
def intro():
    return render_template('introductory.html')

# 主页路由 (需要登录)
@site_views.route('/index')
@login_required
def index():
    # Query for the three most recent posts
    recent_posts = Request.query.order_by(Request.timestamp.desc()).limit(3).all()

    # Query for the top scorers
    scores = db.session.query(
        User.username,
        db.func.sum(Point.points).label('total_points')
    ).join(Point).group_by(User.id).order_by(db.desc('total_points')).all()
    return render_template('index.html', recent_posts=recent_posts, scores=scores, enumerate=enumerate)


@site_views.route('/index-2')
@login_required
def index_2():
    return render_template('index-2.html')

# 画廊页面路由 (需要登录)
@site_views.route('/gallery')
@login_required
def gallery():
    return render_template('gallery.html')

@site_views.route('/post')
@login_required
def post():
    query = request.args.get('query')
    sort_by = request.args.get('sort_by')
    if query:
        requests_query = Request.query.filter(
            Request.title.ilike(f'%{query}%') | Request.description.ilike(f'%{query}%')
        )
    else:
        requests_query = Request.query

    if sort_by == 'date':
        requests = requests_query.order_by(Request.timestamp.desc()).all()
    elif sort_by == 'likes':
        requests = requests_query.outerjoin(Like).group_by(Request.id).order_by(db.func.count(Like.id).desc()).all()
    else:
        requests = requests_query.all()
    comment_form = CommentForm()
    # Get the new request's id from the query parameters
    new_request_id = request.args.get('request_id')
    return render_template('post.html', requests=requests, comment_form=comment_form, new_request_id=new_request_id)


# 单个帖子页面路由 (需要登录)
@site_views.route('/single-post/<int:request_id>')
@login_required
def single_post(request_id):
    request = Request.query.get_or_404(request_id)
    comments = Comment.query.filter_by(request_id=request_id).all()
    comment_form = CommentForm()
    return render_template('single-post.html', request=request, comments=comments, comment_form=comment_form)