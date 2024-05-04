from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
db = SQLAlchemy(app)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

app.app_context().push()  # 创建应用程序上下文

db.create_all()


@app.route('/')
def dashboard():
    requests = Request.query.all()
    return render_template('dashboard.html', requests=requests)

@app.route('/create_request', methods=['GET', 'POST'])
def create_request():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_request = Request(title=title, description=description)
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_request.html')

if __name__ == '__main__':
    app.run(debug=True)
