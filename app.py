from flask import Flask, render_template
import propertyRetrieval
import json

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    suburb = "Hurstville"
    getProperty = propertyRetrieval.get_property_info()
    return getProperty,render_template('index.html')


@app.route('/search')
def search():
    return 'nice'


@app.route('/test')
def test():
    return render_template('another test.html')


if __name__ == '__main__':
    app.run()
