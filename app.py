from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, User, Request
from forms import RegisterForm, LoginForm

app = Flask(__name__)
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

# Process user registration
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
    return render_template('register.html', form=form)

# Process user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')        
    return render_template('login.html', form=form)

# User logout and redirection
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['GET'])
def dashboard():
    query = request.args.get('query')
    requests = Request.query.filter(
        Request.title.ilike(f'%{query}%') | Request.description.ilike(f'%{query}%')
    ).all() if query else Request.query.all()
    return render_template('dashboard.html', requests=requests)

@app.route('/create_request', methods=['GET', 'POST'])
def create_request():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_request = Request(title=title, description=description)
        try:
            db.session.add(new_request)
            db.session.commit()
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            return f"Error adding request: {e}", 500  
    return render_template('create_request.html')


if __name__ == '__main__':
    app.run(debug=True)




