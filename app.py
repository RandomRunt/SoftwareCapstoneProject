from flask import Flask, render_template, redirect, url_for, request
import requests, json, urllib.request
import data_base, house_searching
from wtforms import Form, validators, StringField

# Domain API variables
client_id = 'client_209b71146a72afa869bbf9bc385deefa'
client_secret = 'secret_31598885c06ef62ddb59f51b84bfba76'
auth_url = 'https://auth.domain.com.au/v1/connect/token'
endpoint_url = 'https://api.domain.com.au/v1/'
sandbox_url = 'https://api.domain.com.au/sandbox/v1/listings/residential/_search'

app = Flask(__name__)


class suburb_inputs(Form):
    suburb_input = StringField('Enter a Sydney Suburb:', validators=[validators.required()])


# Other constants
suburblist = ["Abbotsbury", "Abbotsford", "Acacia Gardens", "Agnes Banks", "Airds", "Alexandria", "Alfords Point",
              "Allambie Heights", "Allawah", "Ambarvale", "Annandale", "Annangrove", "Arcadia", "Arncliffe",
              "Arndell Park", "Artarmon", "Ashbury", "Ashcroft", "Ashfield", "Asquith", "Auburn", "Austral",
              "Avalon Beach", "Badgerys Creek", "Balgowlah", "Balgowlah Heights", "Balmain", "Balmain East", "Bangor",
              "Banksia", "Banksmeadow", "Bankstown", "Bankstown Aerodrome", "Barangaroo", "Barden Ridge", "Bardia",
              "Bardwell Park", "Bardwell Valley", "Bass Hill", "Baulkham Hills", "Bayview", "Beacon Hill",
              "Beaconsfield", "Beaumont Hills", "Beecroft", "Belfield", "Bella Vista", "Bellevue Hill", "Belmore",
              "Belrose", "Berala", "Berkshire Park", "Berowra", "Berowra Creek", "Berowra Heights", "Berowra Waters",
              "Berrilee", "Beverley Park", "Beverly Hills", "Bexley", "Bexley North", "Bickley Vale", "Bidwill",
              "Bilgola Beach", "Bilgola Plateau", "Birchgrove", "Birrong", "Blackett", "Blacktown", "Blair Athol",
              "Blairmount", "Blakehurst", "Bligh Park", "Bondi", "Bondi Beach", "Bondi Junction", "Bonnet Bay",
              "Bonnyrigg", "Bonnyrigg Heights", "Bossley Park", "Botany", "Bow Bowing", "Box Hill", "Bradbury",
              "Breakfast Point", "Brighton Le Sands", "Bringelly", "Bronte", "Brooklyn", "Brookvale", "Bundeena",
              "Bungarribee", "Burraneer", "Burwood", "Burwood Heights", "Busby", "Cabarita", "Cabramatta",
              "Cabramatta West", "Caddens", "Cambridge Gardens", "Cambridge Park", "Camden", "Camden South", "Camellia",
              "Cammeray", "Campbelltown", "Camperdown", "Campsie", "Canada Bay", "Canley Heights", "Canley Vale",
              "Canoelands", "Canterbury", "Caringbah", "Caringbah South", "Carlton", "Carnes Hill",
              "Carramar", "Carss Park", "Cartwright", "Castle Cove", "Castle Hill", "Castlecrag", "Castlereagh",
              "Casula", "Catherine Field", "Cattai", "Cawdor", "Cecil Hills", "Cecil Park", "Centennial Park",
              "Central Business District", "Chatswood", "Chatswood West", "Cheltenham", "Cherrybrook", "Chester Hill",
              "Chifley", "Chippendale", "Chipping Norton", "Chiswick", "Chullora", "Church Point", "Claremont Meadows",
              "Clarendon", "Clareville", "Claymore", "Clemton Park", "Clontarf", "Clovelly", "Clyde",
              "Coasters Retreat", "Cobbitty", "Colebee", "Collaroy", "Collaroy Plateau", "Colyton", "Como", "Concord",
              "Concord West", "Condell Park", "Connells Point", "Constitution Hill", "Coogee", "Cornwallis",
              "Cottage Point", "Cowan", "Cranebrook", "Cremorne", "Cremorne Point", "Cromer", "Cronulla", "Crows Nest",
              "Croydon", "Croydon Park", "Cumberland Reach", "Curl Curl", "Currans Hill", "Currawong Beach",
              "Daceyville", "Dangar Island", "Darling Point", "Darlinghurst", "Darlington", "Davidson", "Dawes Point",
              "Dean Park", "Dee Why", "Denham Court", "Denistone", "Denistone East", "Denistone West", "Dharruk",
              "Dolans Bay", "Dolls Point", "Double Bay", "Dover Heights", "Drummoyne", "Duffys Forest",
              "Dulwich Hill", "Dundas", "Dundas Valley", "Dural", "Eagle Vale", "Earlwood", "East Gordon", "East Hills",
              "East Killara", "East Kurrajong", "East Lindfield", "East Ryde", "Eastern Creek", "Eastgardens",
              "Eastlakes", "Eastwood", "Ebenezer", "Edensor Park", "Edgecliff", "Edmondson Park", "Elanora Heights",
              "Elderslie", "Elizabeth Bay", "Elizabeth Hills", "Ellis Lane", "Elvina Bay", "Emerton", "Emu Heights",
              "Emu Plains", "Enfield", "Engadine", "Englorie Park", "Enmore", "Epping", "Ermington", "Erskine Park",
              "Erskineville", "Eschol Park", "Eveleigh", "Fairfield", "Fairfield East", "Fairfield Heights",
              "Fairfield West", "Fairlight", "Fiddletown", "Five Dock", "Flemington", "Forest Glen", "Forest Lodge",
              "Forestville", "Freemans Reach", "Frenchs Forest", "Freshwater", "Galston", "Georges Hall", "Gilead",
              "Girraween", "Gladesville", "Glebe", "Gledswood Hills", "Glen Alpine", "Glendenning", "Glenfield",
              "Glenhaven", "Glenmore Park", "Glenorie", "Glenwood", "Glossodia", "Gordon", "Granville", "Grasmere",
              "Grays Point", "Great Mackerel Beach", "Green Valley", "Greenacre", "Greendale", "Greenfield Park",
              "Greenhills Beach", "Greenwich", "Gregory Hills", "Greystanes", "Grose Vale", "Grose Wold", "Guildford",
              "Guildford West", "Gymea", "Gymea Bay", "Haberfield", "Hammondville", "Harrington Park", "Harris Park",
              "Hassall Grove", "Haymarket", "Heathcote", "Hebersham", "Heckenberg", "Henley", "Hillsdale",
              "Hinchinbrook", "Hobartville", "Holroyd", "Holsworthy", "Homebush", "Homebush West", "Horningsea Park",
              "Hornsby", "Hornsby Heights", "Horsley Park", "Hoxton Park", "Hunters Hill", "Huntingwood",
              "Huntleys Cove", "Huntleys Point", "Hurlstone Park", "Hurstville", "Hurstville Grove", "Illawong",
              "Ingleburn", "Ingleside", "Jamisontown", "Jannali", "Jordan Springs", "Kangaroo Point", "Kareela",
              "Kearns", "Kellyville", "Kellyville Ridge", "Kemps Creek", "Kensington", "Kenthurst", "Kentlyn",
              "Killara", "Killarney Heights", "Kings Langley", "Kings Park", "Kingsford", "Kingsgrove", "Kingswood",
              "Kingswood Park", "Kirkham", "Kirrawee", "Kirribilli", "Kogarah", "Kogarah Bay", "Ku-Ring-Gai Chase",
              "Kurmond", "Kurnell", "Kurraba Point", "Kurrajong", "Kurrajong Hills", "Kyeemagh", "Kyle Bay",
              "La Perouse", "Lakemba", "Lalor Park", "Lane  Cove", "Lane Cove North", "Lane  Cove West", "Lansdowne",
              "Lansvale", "Laughtondale", "Lavender Bay", "Leets Vale", "Leichhardt", "Len Waters Estate", "Leonay",
              "Leppington", "Lethbridge Park", "Leumeah", "Lewisham", "Liberty Grove", "Lidcombe", "Lilli Pilli",
              "Lilyfield", "Lindfield", "Linley Point", "Little Bay", "Liverpool", "Llandilo", "Loftus", "Londonderry",
              "Long Point", "Longueville", "Lovett Bay", "Lower Portland", "Lucas Heights", "Luddenham", "Lugarno",
              "Lurnea", "Macquarie Fields", "Macquarie Links", "Macquarie Park", "Maianbar", "Malabar", "Manly",
              "Manly Vale", "Maraylya", "Marayong", "Maroota", "Maroubra", "Marrickville", "Marsden Park", "Marsfield",
              "Mascot", "Matraville", "Mays Hill", "McCarrs Creek", "McGraths Hill", "McMahons Point", "Meadowbank",
              "Melrose Park", "Menai", "Menangle Park", "Merrylands", "Merrylands West", "Middle Cove", "Middle Dural",
              "Middleton Grange", "Miller", "Millers Point", "Milperra", "Milsons Passage", "Milsons Point",
              "Minchinbury", "Minto", "Minto Heights", "Miranda", "Mona Vale", "Monterey", "Moore Park", "Moorebank",
              "Morning Bay", "Mortdale", "Mortlake", "Mosman", "Mount Annan", "Mount Colah", "Mount Druitt",
              "Mount Ku-Ring-Gai", "Mount Lewis", "Mount Pritchard", "Mount Vernon", "Mulgoa", "Mulgrave",
              "Narellan Vale", "Naremburn", "Narrabeen", "Narraweena", "Narwee", "Nelson", "Neutral Bay", "Newington",
              "Newport", "Newtown", "Normanhurst", "North Balgowlah", "North Bondi", "North Curl Curl", "North Epping",
              "North Kellyville", "North Manly", "North Narrabeen", "North Parramatta", "North Richmond", "North Rocks",
              "North Ryde", "North St Ives", "North St Marys", "North Strathfield", "North Sydney", "North Turramurra",
              "North Willoughby", "North Wahroonga", "Northbridge", "Northmead", "Northwood", "Norwest", "Oakhurst",
              "Oakville", "Oatlands", "Oatley", "Old Guildford", "Old Toongabbie", "Oran Park", "Orchard Hills",
              "Oxford Falls", "Oxley Park", "Oyster Bay", "Paddington", "Padstow", "Padstow Heights", "Pagewood",
              "Palm Beach", "Panania", "Parklea", "Parramatta", "Peakhurst", "Peakhurst Heights", "Pemulwuy",
              "Pendle Hill", "Pennant Hills", "Penrith", "Penshurst", "Petersham", "Phillip Bay", "Picnic Point",
              "Pitt Town", "Pitt Town Bottoms", "Pleasure Point", "Plumpton", "Point Piper", "Port Botany",
              "Port Hacking", "Potts Hill", "Potts Point", "Prairiewood", "Prestons", "Prospect", "Punchbowl", "Putney",
              "Pymble", "Pyrmont", "Quakers Hill", "Queens Park", "Queenscliff", "Raby", "Ramsgate", "Ramsgate Beach",
              "Randwick", "Redfern", "Regents Park", "Regentville", "Revesby", "Revesby Heights", "Rhodes", "Richmond",
              "Richmond Lowlands", "Riverstone", "Riverview", "Riverwood", "Rockdale", "Rodd Point", "Rookwood",
              "Rooty Hill", "Ropes Crossing", "Rose Bay", "Rosebery", "Rosehill", "Roselands", "Rosemeadow",
              "Roseville", "Roseville Chase", "Rossmore", "Rouse Hill", "Royal National Park", "Rozelle", "Ruse",
              "Rushcutters Bay", "Russell Lea", "Rydalmere", "Ryde", "Sackville", "Sackville North", "Sadleir",
              "Sandringham", "Sandy Point", "Sans Souci", "Scheyville", "Schofields", "Scotland Island", "Seaforth",
              "Sefton", "Seven Hills", "Shalvey", "Shanes Park", "Silverwater", "Singletons Mill", "Smeaton Grange",
              "Smithfield", "South Coogee", "South Granville", "South Hurstville", "South Maroota", "South Penrith",
              "South Turramurra", "South Wentworthville", "South Windsor", "Spring Farm", "St Andrews", "St Clair",
              "St Helens Park", "St Ives", "St Ives Chase", "St Johns Park", "St Leonards", "St Marys", "St Peters",
              "Stanhope Gardens", "Stanmore", "Strathfield", "Strathfield South", "Summer Hill", "Surry Hills",
              "Sutherland", "Sydenham", "Sydney Olympic Park", "Sylvania", "Sylvania Waters", "Tamarama", "Taren Point",
              "Telopea", "Tempe", "Tennyson", "Tennyson Point", "Terrey Hills", "The Ponds", "The Rocks", "The Slopes",
              "Thornleigh", "Toongabbie", "Tregear", "Turramurra", "Turrella", "Ultimo", "Varroville", "Vaucluse",
              "Villawood", "Vineyard", "Voyager Point", "Wahroonga", "Waitara", "Wakeley", "Wallacia", "Wareemba",
              "Warrawee", "Warriewood", "Warwick Farm", "Waterfall", "Waterloo", "Watsons Bay", "Wattle Grove",
              "Waverley", "Waverton", "Wedderburn", "Wentworth Point", "Wentworthville", "Werrington",
              "Werrington County", "Werrington Downs", "West Hoxton", "West Killara", "West Lindfield",
              "West Pennant Hills", "West Pymble", "West Ryde", "Westleigh", "Westmead", "Wetherill Park", "Whalan",
              "Whale Beach", "Wheeler Heights", "Wilberforce", "Wiley Park", "Willmot", "Willoughby", "Willoughby East",
              "Windsor", "Windsor Downs", "Winston Hills", "Wisemans Ferry", "Wolli Creek", "Wollstonecraft",
              "Woodbine", "Woodcroft", "Woodpark", "Woollahra", "Woolloomooloo", "Woolooware", "Woolwich", "Woronora",
              "Woronora Heights", "Yagoona", "Yarramundi", "Yarrawarrah", "Yennora", "Yowie Bay", "Zetland"]

access_token = json.loads(requests.post(
    auth_url,
    data={
        "grant_type": "client_credentials",
        "scope": [" ".join([
            "api_demographics_read",
            "api_addresslocators_read",
            "api_properties_read",
            "api_agencies_read",
            "api_suburbperformance_read",
            "api_salesresults_read",
            "api_listings_write",
            "api_listings_read",
            "api_locations_read"
        ])
        ]
    },
    auth=(client_id, client_secret)
).content)
print(access_token["access_token"])


@app.route('/index')
@app.route('/')
def index():
    house_searching.suburb_grab('North Bondi', 'NSW')
    return render_template('index.html')


@app.route('/<street_num>/<street_name>/<suburb>')
def address(street_num, street_name, suburb):
    response = requests.request(
        "GET",
        endpoint_url + "properties/_suggest?terms=" + street_num + "+" + street_name + "+St%1C+" + suburb +
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
        return render_template('404.html')
    else:
        house_searching.suburb_grab(suburb, street_num, street_name, postcode, state)
        data_base_test = data_base.findProperty(property_id)

        if not data_base_test:
            # BLAH BLAH ENTER CODE HERE ONCE IT WORKS
            lower_price = "-"
            upper_price = "-"
            mid_price = "-"

            response = requests.request(
                "GET",
                endpoint_url + "properties/" + property_id,
                headers={'Authorization': 'Bearer ' + access_token["access_token"],
                         'Content-Type': 'application/json'}
            )

            house = response.json()
            print(house)
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
        data_base_test = data_base.findProperty(property_id)
        property = data_base_test[0]

    return render_template("result_of_home_page_search.html", property=property)


@app.route("/suburb_search")
def search_suburb():
    return render_template("suburb_search.html")


@app.route('/suburb/<suburb>')
def suburb_search(suburb):
    print(suburb)
    suburb_check = data_base.findSuburb(suburb)
    suburb_info = suburb_check[0]
    population = [suburb_info[2],suburb_info[3],suburb_info[4],suburb_info[5],suburb_info[6]]
    sales = [suburb_info[9],suburb_info[10],suburb_info[11],suburb_info[12]]
    return render_template("suburb.html", suburb=suburb, suburb_info=suburb_info, population=population, sales=sales)


@app.route("/house", methods=['GET', 'POST'])
def house():
    property_id = ""
    message_name = ""

    form = house_searching.address_inputs(request.form)
    if request.method == 'POST':
        street_name = request.form['street_Name']
        street_num = request.form['street_Num']
        suburb = request.form['suburb']
        response = requests.request(
            "GET",
            endpoint_url + "properties/_suggest?terms=" + street_num + "+" + street_name + "+St%1C+" + suburb +
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
            pass
        else:
            data_base_test = data_base.findProperty(property_id)

            if not data_base_test:
                response = requests.request(
                    "GET",
                    endpoint_url + "properties/" + property_id + "/priceEstimate",
                    headers={'Authorization': 'Bearer ' + access_token["access_token"],
                             'Content-Type': 'application/json'}
                )

                # BLAH BLAH ENTER CODE HERE ONCE IT WORKS
                lower_price = "-"
                upper_price = "-"
                mid_price = "-"
                print(response)

                response = requests.request(
                    "GET",
                    endpoint_url + "properties/" + property_id,
                    headers={'Authorization': 'Bearer ' + access_token["access_token"],
                             'Content-Type': 'application/json'}
                )

                house = response.json()
                print(house)
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
    if property_id == "":
        if request.method == "POST":
            message_name = "Please enter a valid address"
        property = ['', "", "", "", "", "", "-", "-", "-",
                    "https://thumbs.dreamstime.com/b/blur-house-background-vintage-style-44768012.jpg", "", "", "", "",
                    "", "", "", ""]
        print(property[9])

    else:
        data_base_test = data_base.findProperty(property_id)
        property = data_base_test[0]
        print(property)

    return render_template("generichouse.html", message_name=message_name, property=property, form=form)


@app.route("/find_property", methods=['GET', 'POST'])
def find():
    message = ""
    properties = 0
    house_dict = {"listingType": "Sale", }
    location_dict = {}
    form = house_searching.feature_inputs()
    states = house_searching.states[::-1]
    if request.method == "POST":
        suburb = request.form['suburb']
        house_found = request.form.getlist('property_type')
        bedrooms = request.form['bedrooms']
        bathrooms = request.form['bathrooms']
        parking = request.form['parking']
        state = request.form.getlist('stateDropdown')
        house_dict['propertyTypes'] = house_found
        house_dict['minBedrooms'] = bedrooms
        house_dict['minBathrooms'] = bathrooms
        house_dict['minCarspaces'] = parking
        location_dict['state'] = state[0]
        location_dict['region'] = ""
        location_dict["area"] = ""
        location_dict["suburb"] = suburb
        location_dict["postCode"] = ""
        location_dict["postCode"] = ""
        location_dict["postCode"] = ""
        house_dict["location"] = [location_dict]

        print(str(house_dict))

        response = requests.request(
            'POST', endpoint_url + str(house_dict)
            , headers={'Authorization': 'Bearer ' + access_token["access_token"],
                       'Content-Type': 'application/json'})

        print(response)

    return render_template('found_property.html', form=form, states=states)


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    validAccounts = {"username":"password","admin":"admin"}
    if request.method == 'POST':
        if request.form['username'] in validAccounts:
            if request.form['password'] == validAccounts[request.form['username']]:
                return redirect(url_for('index'))
        else:
            error = 'The username or password is invalid.'
    return render_template('login.html', error=error)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    from os import environ
    app.run(debug=False, port=environ.get("PORT", 5000), processes=2)
