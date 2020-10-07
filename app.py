from flask import Flask, render_template, request
import requests, json
from flask_bootstrap import Bootstrap
import data_base
from wtforms import Form, validators, StringField

# Domain API variables
client_id = 'client_209b71146a72afa869bbf9bc385deefa'
client_secret = 'secret_31598885c06ef62ddb59f51b84bfba76'
auth_url = 'https://auth.domain.com.au/v1/connect/token'
endpoint_url = 'https://api.domain.com.au/v1/'

# specific property id
property_id = "NT-7996-GP"


app = Flask(__name__)
bootstrap = Bootstrap(app)


class suburb_inputs(Form):
    suburb_input = StringField('Full Name:', validators=[validators.required()])


if __name__ == '__main__':
    app.run()


@app.route('/')
@app.route('/index')
def index():
    access_token = json.loads(requests.post(
        auth_url,
        data={
            "grant_type": "client_credentials",
            "scope": [" ".join([
                "api_properties_read",
                "api_demographics_read",
                "api_addresslocators_read",
                "api_suburbperformance_read",
                "api_locations_read", ])
            ]
        },
        auth=(client_id, client_secret)
    ).content)
    print(access_token["access_token"])
    response = requests.request(
        "GET",
        endpoint_url + "properties/" + property_id,
        headers={'Authorization': 'Bearer ' + access_token["access_token"], 'Content-Type': 'application/json'}
    )
    print(response.json())
    return render_template('index.html')


@app.route('/home')
def home():
    render_template("home.html")


@app.route('/suburb_search', methods=['GET', 'POST'])
def suburb_search():
    suburb = ""
    form = suburb_inputs(request.form)
    message_name = ''

    if request.method == 'POST':
        suburb = request.form['suburb_input']
    suburb_check = data_base.findSuburb(suburb)

    if not suburb_check:
        message_name = 'Please enter a valid suburb'
        print('no')
    else:
        print("yeet")

    return render_template("suburb.html", message_name=message_name, form=form)


@app.route('/search')
def search():
    return 'nice'


#Testing charting library
@app.route('/test')
def test():
    adict = {"type": "line", "title":"test"}
    labels = ["A","B","C","D","E","F"]
    data = [{"label":"1","data":[120,130,139,162,153,149],},{"label":"2","data":[238,254,279,289,291,305]}]
    send = [adict,labels,data]
    return render_template('charttest.html', nchart=send)


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')