from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
# config URL for database
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:1q2w3e4r@localhost:3306/flask_website"
db = SQLAlchemy(app)


class PersonalInfo(db.Model):
    id = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(75))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)

    def __repr__(self):
        return f"(('id', '{self.id}'), ('name', '{self.name}'), ('gender', '{self.gender}'), ('age', '{self.age}'))"


@app.route('/')
def index():
    db.create_all()
    return render_template('index.html')


@app.route('/add')
def add():
    return render_template('Add.html')


@app.route('/add/submit', methods=['POST'])
def add_submit():
    info = PersonalInfo(
        id=request.form['id'],
        name=request.form['name'],
        gender=request.form['gender'],
        age=request.form['age']
    )
    db.session.add(info)
    try:
        db.session.commit()
    except:
        pass

    return redirect(url_for('add_success'))


@app.route('/add/submit/success')
def add_success():
    return "<h1> information has successfully stored! </h1>"


@app.route('/query')
def query():
    return render_template('Query.html')


@app.route('/query/submit', methods=['POST'])
def query_submit():
    info_id = request.form['info_id']
    res = dict(eval(f"{PersonalInfo.query.get(info_id)}"))
    response = make_response(json.dumps(res))
    response.mimetype = 'application/json'
    return response