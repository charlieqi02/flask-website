from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
# config URL for database
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1q2w3e4r@localhost:3306/flask_website"
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200))
    name = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)

    def __repr__(self):
        return {
            "id": self.id,
            "body": self.body,
            "name": self.name,
            "timestamp": self.timestamp
        }


@app.route('/')
def index():
    db.create_all()
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    len_of_messages = len(messages)
    return render_template('index.html', messages=messages, len_of_messages=len_of_messages)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    message = Message(    
        name = request.form['name'],
        body = request.form['body']
    )
    db.session.add(message)
    db.session.commit()
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    len_of_messages = len(messages)
    return render_template('index.html', messages=messages, len_of_messages=len_of_messages)