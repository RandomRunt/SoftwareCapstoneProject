import requests
import json
import app

client_id = 'client_209b71146a72afa869bbf9bc385deefa'
client_secret = 'secret_31598885c06ef62ddb59f51b84bfba76'
scopes = 'api_agencies_read api_listings_read'
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

def get_property_info():
    response = requests.post(auth_url, data={
                        'client_id':client_id,
                        'client_secret':client_secret,
                        'grant_type':'client_credentials',
                        'scope':scopes,
                        'Content-Type':'text/json'
                        })
    json_response = response.json()
    access_token = json_response['access_token']
    print(access_token)
    auth = {'Authorization':'Bearer ' + access_token}
    url = "https://api.domain.com.au/v1/listings/residential/_search"
    request = requests.post(url, data=search_parameters, headers=auth)
    details = request.json()
    print(details)
