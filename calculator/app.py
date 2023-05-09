from flask import Flask, render_template, request, redirect, url_for, make_response
import sympy


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simple')
def simple():
    return render_template('simple.html')

@app.route('/advanced')
def advanced():
    return render_template('advanced.html')