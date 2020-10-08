import sqlite3


def createTable():
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE properties_data_base(property_id text, street_name text, street_num integer, suburb text, 
    street_type text, state text, lower_price integer, upper_price integer, mid_price integer, image text, 
    lat_coordinate text, long_coordinate text, property_type text, bedrooms integer, bathrooms integer, 
    car_spaces integer  )''')

    conn.commit()
    conn.close()


def addProperty(property_id, street_name, street_num, suburb, street_type, state, lower_price, upper_price, mid_price,
                image, lat_coordinate, long_coordinate, property_type, bedrooms, bathrooms, car_spaces, areaSize):
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    c.execute("INSERT INTO properties_data_base (property_id, street_name, street_num, suburb, street_type, state, "
              "lower_price, upper_price, mid_price, image, lat_coordinate, long_coordinate, property_type, bedrooms, "
              "bathrooms, car_spaces, areaSize) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (property_id, street_name, street_num, suburb, street_type, state, lower_price, upper_price, mid_price,
               image, lat_coordinate, long_coordinate, property_type, bedrooms, bathrooms, car_spaces, areaSize))

    conn.commit()
    conn.close()


def addSuburb(suburb_id, suburb, age_0_to_4, age_5_to_19, age_20_to_39, age_40_to_59, age_60_plus, postcode, state,
              properties_sold, clearance_rate, median_sale, total_sale, population):
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO suburbs (suburb_id, suburb, age_0_to_4, age_5_to_19, age_20_to_39, age_40_to_59, age_60_plus, "
        "postcode, state, properties_sold, clearance_rate, median_sale, total_sale, population) VALUES (?, ?, ?, ?, ?,"
        " ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (suburb_id, suburb, age_0_to_4, age_5_to_19, age_20_to_39, age_40_to_59, age_60_plus, postcode, state,
         properties_sold, clearance_rate, median_sale, total_sale, population))
    conn.commit()
    conn.close()


def findSuburb(suburb):
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    houses_in_suburbs = []
    for row in c.execute('SELECT * FROM suburbs WHERE suburb=?', (suburb,)):
        houses_in_suburbs.append(row)
    return houses_in_suburbs
    conn.close()


def findProperty(property_id):
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    property = []
    for row in c.execute('SELECT * FROM properties_data_base WHERE suburb=?', (property_id,)):
        property.append(row)
    return property
    conn.close()