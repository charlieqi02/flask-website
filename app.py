from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# config URL for database
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1q2w3e4r@localhost:3306/flask_website"
db = SQLAlchemy(app)


class PersonalInfo(db.Model):
    __name__ = 'per_infotest'
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(75))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)

    def __repr__(self):
        return '<PersonalInfoTest id>'


@app.route('/')
def index():
    db.create_all()
    return render_template('index.html')


@app.route('/submit/success')
def success():
    return "<h1> information has successfully stored! </h1>"


@app.route('/submit', methods=['POST'])
def submit():
    info = PersonalInfo(
        id=request.form['id'],
        name=request.form['name'],
        gender=request.form['gender'],
        age=request.form['age']
    )
    db.session.add(info)
    db.session.commit()

    return redirect(url_for('success'))