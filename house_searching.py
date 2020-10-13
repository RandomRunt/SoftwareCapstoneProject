from wtforms import Form, validators, StringField, SelectMultipleField, widgets, RadioField
from wtforms.validators import DataRequired
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


class MultiCheckboxField(SelectMultipleField): #Nathan Roland
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class feature_inputs(Form): #didnt work
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


class address_inputs(Form):  #didnt work
    unit_Number = StringField('Enter a unit number (optional): ')
    street_Num = StringField('Enter the street number: ', validators=[validators.required(int)])
    street_Name = StringField('Enter the street name: ', validators=[validators.required()])
    suburb = StringField('Enter the suburb: ', validators=[validators.required()])


def suburb_grab(suburb, state): #Nathan Roland
    suburb_check = data_base.findSuburb(suburb)

    if not suburb_check:
        response_4 = requests.request(
            'GET', endpoint_url + "addressLocators?searchLevel=Suburb&suburb=" + suburb + "&state=NSW"
            , headers={'Authorization': 'Bearer ' + access_token["access_token"],
                       'Content-Type': 'application/json'})

        properties = response_4.json()[0]
        addressComponents = properties.get('addressComponents')[1]
        postcode = addressComponents.get('shortName')
        suburb_levels = properties.get('ids')[0]
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

        print('done')

        response = requests.request(
            "GET",
            endpoint_url + "suburbPerformanceStatistics?state=nsw&suburbId=" + str(suburb_id) + "&propertyCategory"
                                                                                                "=house"
                                                                                                "&chronologicalSpan=12"
                                                                                                "&tPlusFrom=1&tPlusTo=3"
                                                                                                "&values"
                                                                                                "=HighestSoldPrice"
                                                                                                "%2CLowestSoldPrice",
            headers={'Authorization': 'Bearer ' + access_token["access_token"],
                     'Content-Type': 'application/json'}
        )
        start = response.json()
        series = start.get('series')

        series_info = series.get('seriesInfo')

        values = series_info[0]
        print(values)
        values_2018 = values.get('values')

        median_sold_price_2018 = values_2018.get('medianSoldPrice')
        number_sold_2018 = values_2018.get('numberSold')
        highest_sold_price_2018 = values_2018.get('highestSoldPrice')
        lowest_sold_price_2018 = values_2018.get('lowestSoldPrice')
        percentile_sold_price_5_2018 = values_2018.get('5thPercentileSoldPrice')
        percentile_sold_price_25_2018 = values_2018.get('25thPercentileSoldPrice')
        percentile_sold_price_75_2018 = values_2018.get('75thPercentileSoldPrice')
        percentile_sold_price_95_2018 = values_2018.get('95thPercentileSoldPrice')
        print(median_sold_price_2018, number_sold_2018, highest_sold_price_2018, lowest_sold_price_2018,
              percentile_sold_price_5_2018, percentile_sold_price_25_2018, percentile_sold_price_75_2018,
              percentile_sold_price_95_2018)

        values = series_info[1]
        print(values)
        values_2019 = values.get('values')
        median_sold_price_2019 = values_2019.get('medianSoldPrice')
        number_sold_2019 = values_2019.get('numberSold')
        highest_sold_price_2019 = values_2019.get('highestSoldPrice')
        lowest_sold_price_2019 = values_2019.get('lowestSoldPrice')
        percentile_sold_price_5_2019 = values_2019.get('5thPercentileSoldPrice')
        percentile_sold_price_25_2019 = values_2019.get('25thPercentileSoldPrice')
        percentile_sold_price_75_2019 = values_2019.get('75thPercentileSoldPrice')
        percentile_sold_price_95_2019 = values_2019.get('95thPercentileSoldPrice')

        values = series_info[2]
        print(values)
        values_2020 = values.get('values')
        median_sold_price_2020 = values_2020.get('medianSoldPrice')
        number_sold_2020 = values_2020.get('numberSold')
        highest_sold_price_2020 = values_2020.get('highestSoldPrice')
        lowest_sold_price_2020 = values_2020.get('lowestSoldPrice')
        percentile_sold_price_5_2020 = values_2020.get('5thPercentileSoldPrice')
        percentile_sold_price_25_2020 = values_2020.get('25thPercentileSoldPrice')
        percentile_sold_price_75_2020 = values_2020.get('75thPercentileSoldPrice')
        percentile_sold_price_95_2020 = values_2020.get('95thPercentileSoldPrice')

        data_base.addSuburb(suburb_id, suburb, age_0_to_4, age_5_to_19, age_20_to_39, age_40_to_59, age_60_plus,
                            postcode,
                            state, population, median_sold_price_2018, number_sold_2018, highest_sold_price_2018,
                            lowest_sold_price_2018, percentile_sold_price_5_2018, percentile_sold_price_25_2018,
                            percentile_sold_price_75_2018, percentile_sold_price_95_2018, median_sold_price_2019,
                            number_sold_2019, highest_sold_price_2019, lowest_sold_price_2019,
                            percentile_sold_price_5_2019, percentile_sold_price_25_2019, percentile_sold_price_75_2019,
                            percentile_sold_price_95_2019, median_sold_price_2020, number_sold_2020,
                            highest_sold_price_2020,
                            lowest_sold_price_2020, percentile_sold_price_5_2020, percentile_sold_price_25_2020,
                            percentile_sold_price_75_2020, percentile_sold_price_95_2020)
