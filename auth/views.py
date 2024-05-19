from . import auth
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from .forms import RegisterForm, LoginForm
from models import User, Point, db

# Register
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('New user has been created!')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error: ' + str(e), 'error')
            print('Error: ' + str(e))
    return render_template('register.html', form=form)

# User login interface
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            today = date.today()
            if not Point.query.filter_by(user_id=user.id, date=today, type='login').first():
                point = Point(user_id=user.id, date=today, points=1, type='login')
                db.session.add(point)
                db.session.commit()
            return redirect(url_for('site_views.index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

# Logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('site_views.intro'))