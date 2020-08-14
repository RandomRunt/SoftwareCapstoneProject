from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


def search():
    return 'nice'


@app.route('/test')
def test():
    return render_template('another test.html')


if __name__ == '__main__':
    app.run()
