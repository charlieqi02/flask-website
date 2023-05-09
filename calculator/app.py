from flask import Flask, render_template, request, send_file
from latex2sympy2 import latex2latex


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/simple')
def simple():
    return render_template('simple.html')


# example: "\frac{d}{dx} \int^{x}_{0} f(x) dx"
@app.route('/advanced', methods=['GET', 'POST'])
def advanced():
    if request.method == 'POST':
        input_exps = request.form['expression']
        output_exps = latex2latex(input_exps)
        return render_template('advanced.html', 
                    input=f"\[ {input_exps} \]", output=f"\[ {output_exps} \]")

    return render_template('advanced.html')