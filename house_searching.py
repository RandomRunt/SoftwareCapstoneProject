from wtforms import Form, validators, StringField
import data_base

class address_inputs(Form):
    unit_Number = StringField('Enter a unit number (optional): ')
    street_Num = StringField('Enter the street number: ', validators=[validators.required(int)])
    street_Name = StringField('Enter the street name: ', validators=[validators.required()])
    suburb = StringField('Enter the suburb: ', validators=[validators.required()])



#
# suburb_check = data_base.findSuburb(suburb)
#
#     if not suburb_check:
#         response_1 = requests.request(
#             "GET",
#             endpoint_url + "salesResults/Sydney/listings",
#             headers={'Authorization': 'Bearer ' + access_token["access_token"], 'Content-Type': 'application/json'}
#         )
#         sales_result = response_1.json()
#         street_num = ''
#         street_name = ''
#
#         for row in sales_result:
#             if row.get('suburb') == suburb:
#                 street_num = row.get('streetNumber')
#                 street_name = row.get('streetName')
#                 state = row.get('state').upper()
#                 street_type = row.get('streetType')
#                 postcode = row.get('postcode')
#                 suburb = row.get('suburb')
#                 print(street_num, street_name, state, postcode, street_type, suburb)
#
#         if postcode == '-':
#             message_name = 'Please enter a valid Sydney suburb'
#         else:
#             response_4 = requests.request(
#                 "GET",
#                 endpoint_url + "addressLocators?searchLevel=Address&streetNumber=" + street_num + "&streetName="
#                 + street_name + "&streetType=Rd&suburb=" + suburb + "&state=NSW&postcode=" + postcode,
#                 headers={'Authorization': 'Bearer ' + access_token["access_token"], 'Content-Type': 'application/json'}
#             )
#             print(response_4.json())
#
#             if str(response_4.json()) == "{'message': '[]'}":
#                 message_name = 'We do not have information on ' + suburb + \
#                                ' at the moment, please enter another Sydney suburb'
#             else:
#                 properties = response_4.json()[0]
#                 suburb_levels = properties.get('ids')[2]
#                 suburb_id = suburb_levels.get('id')
#
#                 response_2 = requests.request(
#                     "GET",
#                     endpoint_url + "demographics?level=Suburb&id=" + str(suburb_id) + "&types=AgeGroupOfPopulation",
#                     headers={'Authorization': 'Bearer ' + access_token["access_token"],
#                              'Content-Type': 'application/json'}
#                 )
#                 age_demographics = (response_2.json().get('demographics'))[0]
#                 indepth = age_demographics.get('items')
#
#                 age_0_to_4 = indepth[0].get('value')
#                 age_5_to_19 = indepth[2].get('value')
#                 age_20_to_39 = indepth[4].get('value')
#                 age_40_to_59 = indepth[3].get('value')
#                 age_60_plus = indepth[1].get('value')
#                 population = age_demographics.get('total')
#
#                 response_3 = requests.request(
#                     "GET",
#                     endpoint_url + "salesResults/Sydney",
#                     headers={'Authorization': 'Bearer ' + access_token["access_token"],
#                              'Content-Type': 'application/json'}
#                 )
#                 properties_sold = response_3.json().get("numberSold")
#                 total_sale = response_3.json().get("totalSales")
#                 median_sale = response_3.json().get("median")
#                 clearance_rate = response_3.json().get("adjClearanceRate")
#                 print('done')
#
#                 data_base.addSuburb(suburb_id, suburb, age_0_to_4, age_5_to_19, age_20_to_39, age_40_to_59, age_60_plus,
#                                     postcode, state, properties_sold, clearance_rate, median_sale, total_sale,
#                                     population)