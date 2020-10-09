from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import Form, validators, StringField, SelectMultipleField, widgets, DecimalField, RadioField
from wtforms.validators import ValidationError, DataRequired
from wtforms.widgets import ListWidget, CheckboxInput

import data_base
import requests, json

# Domain API variables
client_id = 'client_209b71146a72afa869bbf9bc385deefa'
client_secret = 'secret_31598885c06ef62ddb59f51b84bfba76'
auth_url = 'https://auth.domain.com.au/v1/connect/token'
endpoint_url = 'https://api.domain.com.au/v1/'

access_token = json.loads(requests.post(
    auth_url,
    data={
        "grant_type": "client_credentials",
        "scope": [" ".join([
            "api_properties_read",
            "api_demographics_read",
            "api_addresslocators_read",
            "api_properties_read",
            "api_suburbperformance_read",
            "api_salesresults_read",
            "api_locations_read"
        ])
        ]
    },
    auth=(client_id, client_secret)
).content)

states = ['NSW', 'VIC', 'WA', 'SA', 'NT', 'CBR', 'QLD', 'TAS']


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class feature_inputs(Form):
    suburb = StringField('Enter a suburb: ', validators=[validators.required()])

    property_type = MultiCheckboxField('Property type: ', choices=[('House', 'House'), ('NewApartments', 'Apartment'),
                                                                   ('Townhouse', 'Townhouse'), ('Land', 'Land'),
                                                                   ('Retirement', 'Retirement')],
                                       validators=[DataRequired()])
    bedrooms = RadioField('Bedrooms: ', choices=[(1, '1+'), (2, '2+'), (3, '3+'), (4, '4+'), (5, '5+')],
                          validators=[validators.required()])
    parking = RadioField('Parking: ', choices=[(1, '1+'), (2, '2+'), (3, '3+'), (4, '4+'), (5, '5+')],
                         validators=[validators.required()])
    bathrooms = RadioField('Bathrooms: ', choices=[(1, '1+'), (2, '2+'), (3, '3+'), (4, '4+'), (5, '5+')],
                           validators=[validators.required()])


class address_inputs(Form):
    unit_Number = StringField('Enter a unit number (optional): ')
    street_Num = StringField('Enter the street number: ', validators=[validators.required(int)])
    street_Name = StringField('Enter the street name: ', validators=[validators.required()])
    suburb = StringField('Enter the suburb: ', validators=[validators.required()])


def suburb_grab(suburb, street_num, street_name, postcode, state):
    suburb_check = data_base.findSuburb(suburb)

    if not suburb_check:
        if state == 'NSW':
            response_4 = requests.request(
                "GET",
                endpoint_url + "addressLocators?searchLevel=Address&streetNumber=" + street_num + "&streetName="
                + street_name + "&streetType=Rd&suburb=" + suburb + "&state=NSW&postcode=" + postcode,
                headers={'Authorization': 'Bearer ' + access_token["access_token"], 'Content-Type': 'application/json'}
            )
            print(response_4.json())

            if str(response_4.json()) == "{'message': '[]'}":
                pass
            else:
                properties = response_4.json()[0]
                suburb_levels = properties.get('ids')[2]
                suburb_id = suburb_levels.get('id')

                response_2 = requests.request(
                    "GET",
                    endpoint_url + "demographics?level=Suburb&id=" + str(suburb_id) + "&types=AgeGroupOfPopulation",
                    headers={'Authorization': 'Bearer ' + access_token["access_token"],
                             'Content-Type': 'application/json'}
                )
                age_demographics = (response_2.json().get('demographics'))[0]
                indepth = age_demographics.get('items')

                age_0_to_4 = indepth[0].get('value')
                age_5_to_19 = indepth[2].get('value')
                age_20_to_39 = indepth[4].get('value')
                age_40_to_59 = indepth[3].get('value')
                age_60_plus = indepth[1].get('value')
                population = age_demographics.get('total')

                response_3 = requests.request(
                    "GET",
                    endpoint_url + "salesResults/Sydney",
                    headers={'Authorization': 'Bearer ' + access_token["access_token"],
                             'Content-Type': 'application/json'}
                )
                properties_sold = response_3.json().get("numberSold")
                total_sale = response_3.json().get("totalSales")
                median_sale = response_3.json().get("median")
                clearance_rate = response_3.json().get("adjClearanceRate")
                print('done')

                data_base.addSuburb(suburb_id, suburb, age_0_to_4, age_5_to_19, age_20_to_39, age_40_to_59, age_60_plus,
                                    postcode, state, properties_sold, clearance_rate, median_sale, total_sale,
                                    population)
