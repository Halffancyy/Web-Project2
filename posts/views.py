from . import posts
from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, User, Request, Like, Point, UserDailyActivity
from .forms import RequestForm
from datetime import date

# 创建新请求的页面 (需要登录)
@posts.route('/create_request', methods=['GET', 'POST'])
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
            return redirect(url_for('site_views.post'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding request: {e}', 'error')
    
    return render_template('create_request.html', form=form)

# 点赞请求的接口 (需要登录)
@posts.route('/like/<int:request_id>', methods=['POST'])
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
