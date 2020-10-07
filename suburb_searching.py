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

print(response)