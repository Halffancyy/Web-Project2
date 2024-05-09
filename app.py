from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Request

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

# Process user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email)
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            return f"Error creating user: {e}", 500
    return render_template('register.html')

# Process user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # 这里应实现登录逻辑，例如设置 session
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

# User logout and redirection
@app.route('/logout')
def logout():
    # 这里应清除 session
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




