from flask import Flask, render_template, request, redirect, url_for
import mysql.connector


app = Flask(__name__, template_folder='templates')

# connect to mysql
conn = mysql.connector.connect(
    user = "root",
    password = "1q2w3e4r",
    host = "localhost",
    database = 'personal_info',
    auth_plugin = 'mysql_native_password'
)

# create user table
cursor = conn.cursor()
# add primary key to this table in order not to store the same info
cursor.execute("CREATE TABLE IF NOT EXISTS \
                personal_info(\
                  name      VARCHAR(255), \
                  gender    VARCHAR(255), \
                  age       INT, \
                  PRIMARY KEY (name, gender, age));") 
cursor.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit/success')
def success():
    return "<h1> information has successfully stored! </h1>"


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    gender = request.form['gender']
    age = request.form['age']

    # inser user info
    cursor = conn.cursor()
    # keep table clean and simple
    cursor.execute(f'INSERT IGNORE INTO personal_info VALUE ("{name}","{gender}",{age})')
    conn.commit()
    cursor.close()

    return redirect(url_for('success'))





if __name__ == "__main__":
    app.run()