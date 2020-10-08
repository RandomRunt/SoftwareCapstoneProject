from flask import Flask, render_template, request
import requests, json
import urllib.request

import data_base, house_searching
from wtforms import Form, validators, StringField

# Domain API variables
client_id = 'client_209b71146a72afa869bbf9bc385deefa'
client_secret = 'secret_31598885c06ef62ddb59f51b84bfba76'
auth_url = 'https://auth.domain.com.au/v1/connect/token'
endpoint_url = 'https://api.domain.com.au/v1/'

app = Flask(__name__)


class suburb_inputs(Form):
    suburb_input = StringField('Enter a Sydney Suburb:', validators=[validators.required()])


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
print(access_token["access_token"])


@app.route('/')
@app.route('/index')
def index():
    property_id = "XJ-5205-DL"
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

    age_0_to_4 = '-'
    age_5_to_19 = '-'
    age_20_to_39 = '-'
    age_40_to_59 = '-'
    age_60_plus = '-'
    postcode = '-'
    state = '-'
    properties_sold = '-'
    clearance_rate = '-'
    median_sale = '-'
    total_sale = '-'
    population = '-'

    if request.method == 'POST':
        suburb = request.form['suburb_input']

    print(suburb)
    suburb_check = data_base.findSuburb(suburb)

    if not suburb_check:
        response_1 = requests.request(
            "GET",
            endpoint_url + "salesResults/Sydney/listings",
            headers={'Authorization': 'Bearer ' + access_token["access_token"], 'Content-Type': 'application/json'}
        )
        sales_result = response_1.json()
        street_num = ''
        street_name = ''

        for row in sales_result:
            if row.get('suburb') == suburb:
                street_num = row.get('streetNumber')
                street_name = row.get('streetName')
                state = row.get('state').upper()
                street_type = row.get('streetType')
                postcode = row.get('postcode')
                suburb = row.get('suburb')
                print(street_num, street_name, state, postcode, street_type, suburb)

        if postcode == '-':
            message_name = 'Please enter a valid Sydney suburb'
        else:
            response_4 = requests.request(
                "GET",
                endpoint_url + "addressLocators?searchLevel=Address&streetNumber=" + street_num + "&streetName="
                + street_name + "&streetType=Rd&suburb=" + suburb + "&state=NSW&postcode=" + postcode,
                headers={'Authorization': 'Bearer ' + access_token["access_token"], 'Content-Type': 'application/json'}
            )
            print(response_4.json())

            if str(response_4.json()) == "{'message': '[]'}":
                message_name = 'We do not have information on ' + suburb + \
                               ' at the moment, please enter another Sydney suburb'
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

    else:
        suburb_info = suburb_check[0]
        age_0_to_4 = suburb_info[1]
        age_5_to_19 = suburb_info[2]
        age_20_to_39 = suburb_info[3]
        age_40_to_59 = suburb_info[4]
        age_60_plus = suburb_info[5]
        postcode = suburb_info[6]
        state = suburb_info[7]
        properties_sold = suburb_info[8]
        clearance_rate = suburb_info[9]
        median_sale = suburb_info[10]
        total_sale = suburb_info[11]
        population = suburb_info[12]
        print("yeet")

    return render_template("suburb.html", suburb=suburb, message_name=message_name, form=form, age_0_to_4=age_0_to_4,
                           age_5_to_19=age_5_to_19, age_20_to_39=age_20_to_39, age_40_to_59=age_40_to_59,
                           age_60_plus=age_60_plus, postcode=postcode, state=state, properties_sold=properties_sold,
                           clearance_rate=clearance_rate, median_sale=median_sale, total_sale=total_sale,
                           population=population)


@app.route("/house", methods=['GET', 'POST'])
def house():
    message_name = ''
    street_name = ""
    street_num = ""
    suburb = ""
    property_id = ""
    street_type = ""
    state = ""
    lower_price = "-"
    upper_price = "-"
    mid_price = "-"
    image = ""
    lat_coordinate = ""
    long_coordinate = ""
    property_type = ""
    bedrooms = ""
    bathrooms = ""
    car_spaces = ""
    areaSize = ""
    postcode = ""

    form = house_searching.address_inputs(request.form)
    if request.method == 'POST':
        street_name = request.form['street_Name']
        street_num = request.form['street_Num']
        suburb = request.form['suburb']
        response = requests.request(
            "GET",
            endpoint_url + "properties/_suggest?terms=" + street_num + "+" + street_name + "+St%2C+" + suburb +
            "&channel=All",
            headers={'Authorization': 'Bearer ' + access_token["access_token"], 'Content-Type': 'application/json'}
        )
        full_address = response.json()[0]
        property_id = full_address.get('id')
        addressComponents = full_address.get('addressComponents')

        street_name = addressComponents.get('streetName')
        street_num = addressComponents.get('streetNumber')
        suburb = addressComponents.get('suburb')

        street_type = addressComponents.get('streetTypeLong')
        postcode = addressComponents.get('postcode')
        state = addressComponents.get('state')
        print(property_id)
        if property_id == "":
            message_name = "Please enter a valid property"
        else:
            house_searching.suburb_grab(suburb, street_num, street_name, postcode, state)
            data_base_test = data_base.findProperty(property_id)

            if not data_base_test:
                response = requests.request(
                    "GET",
                    endpoint_url + "properties/" + property_id + "/priceEstimate",
                    headers={'Authorization': 'Bearer ' + access_token["access_token"], 'Content-Type': 'application/json'}
                )

                # BLAH BLAH ENTER CODE HERE ONCE IT WORKS
                print(response)

                response = requests.request(
                    "GET",
                    endpoint_url + "properties/" + property_id,
                    headers={'Authorization': 'Bearer ' + access_token["access_token"], 'Content-Type': 'application/json'}
                )

                house = response.json()
                coordinate = house.get('addressCoordinate')
                lat_coordinate = coordinate.get('lat')
                long_coordinate = coordinate.get('lon')
                areaSize = house.get('areaSize')
                property_type = house.get('propertyCategory')
                bedrooms = house.get('bedrooms')
                bathrooms = house.get('bathrooms')
                car_spaces = house.get('carSpaces')
                images = house.get('photos')
                if str(images) == '[]':
                    image = 'https://thumbs.dreamstime.com/b/blur-house-background-vintage-style-44768012.jpg'
                else:
                    image1 = images[0]
                    image = image1.get('fullUrl')

                data_base.addProperty(property_id, street_name, street_num, suburb, street_type, state, lower_price,
                                      upper_price, mid_price, image, lat_coordinate, long_coordinate, property_type,
                                      bedrooms, bathrooms, car_spaces, areaSize, postcode)
            else:
                property = data_base_test[0]
                print(property)
                street_name = property[1]
                street_num = property[2]
                suburb = property[3]
                street_type = property[4]
                state = property[5]
                lower_price = property[6]
                upper_price = property[7]
                mid_price = property[8]
                image = property[9]
                lat_coordinate = property[10]
                long_coordinate = property[11]
                property_type = property[12]
                bedrooms = property[13]
                bathrooms = property[14]
                car_spaces = property[15]
                areaSize = property[16]
                postcode = property[17]

    return render_template("generichouse.html", street_name=street_name, street_num=street_num, suburb=suburb,
                           form=form, street_type=street_type, state=state, lower_price=lower_price,
                           upper_price=upper_price, mid_price=mid_price, images_of_house=image,
                           lat_coordinate=lat_coordinate, long_coordinate=long_coordinate, property_type=property_type,
                           bedrooms=bedrooms, bathrooms=bathrooms, car_spaces=car_spaces, areaSize=areaSize, postcode=
                           postcode, message_name=message_name)


# Testing charting library
@app.route('/test')
def test():
    adict = {"type": "line", "title": "test"}
    labels = ["A", "B", "C", "D", "E", "F"]
    data = [{"label": "1", "data": [120, 130, 139, 162, 153, 149], },
            {"label": "2", "data": [238, 254, 279, 289, 291, 305]}]
    send = [adict, labels, data]
    return render_template('charttest.html', nchart=send)


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
