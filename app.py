from flask import Flask, render_template
import requests
import json

# Domain API variables
client_id = 'client_209b71146a72afa869bbf9bc385deefa'
client_secret = 'secret_31598885c06ef62ddb59f51b84bfba76'
scopes = 'api_properties_read'
auth_url = 'https://auth.domain.com.au/v1/connect/token'
search_parameters = {
  "listingType": "Sale",
  "locations": [
    {
      "state": "NSW",
      "suburb": "Hurstville",
      "postcode": 2220,
      "includeSurroundingSuburbs": True
    }
  ]
}

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    response = requests.post(auth_url, data={
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': scopes,
        'Content-Type': 'text/json'
    })
    json_response = response.json()
    access_token = json_response['access_token']
    print(access_token)
    auth = {'Authorization': 'Bearer ' + access_token}
    url = "https://api.domain.com.au/v1/properties/RF-8884-AK"
    request = requests.get(url, headers=auth)
    print(request)
    details = request.json()
    print(details)
    return render_template('index.html')


@app.route('/search')
def search():
    return 'nice'


if __name__ == '__main__':
    app.run()
