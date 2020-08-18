from flask import Flask, render_template
from dataclasses import dataclass

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    return 'nice'


@app.route('/test')
def test():
    dict = {"A":1,"B":2,"C":3,"D":4}
    return render_template('charttest.html', jsdict=dict)


if __name__ == '__main__':
    app.run()
