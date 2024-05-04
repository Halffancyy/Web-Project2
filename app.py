from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
db = SQLAlchemy(app)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()

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
