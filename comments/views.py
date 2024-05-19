from . import comments
from flask import request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Comment, UserDailyActivity, Point
from comments.forms import CommentForm
from datetime import date

# API endpoint for commenting on requests (requires login)
@comments.route('/comment/<int:request_id>', methods=['POST'])
@login_required
def comment_request(request_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, request_id=request_id)
        today = date.today()

         # Get the user's activity record for the current day
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
    return redirect(url_for('site_views.single_post', request_id=request_id))

@comments.route('/delete_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment and current_user == comment.user:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('site_views.single_post', request_id=comment.request_id))