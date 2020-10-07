import sqlite3


def createTable():
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE property_ids(property_id text, address text, price integer, coordinate text, 
    domain_id text)''')
    c.execute('''CREATE TABLE property_features(property_type text, bedrooms integer, bathrooms integer, car_spaces 
    integer, )''')
    c.execute('''CREATE TABLE suburbs(suburb_id text, suburb text, age_0_to_4 integer, age_5_to_19 integer, age_20_to_39 
    integer, age_40_to_59 integer, age_60_plus integer, postcode integer, state text, properties_sold integer, 
    clearance_rate integer, median_sale integer, total_sale integer)''')
    conn.commit()
    conn.close()


def addProperty(property_id, address, price, coordinate, domain_id, property_type, bedrooms, bathrooms, car_spaces):
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    c.execute("INSERT INTO property_ids (property_id, address, price, coordinate, domain_id) VALUES (?, ?)",
              (property_id, address, price, coordinate, domain_id))
    c.execute("INSERT INTO property_features (property_type, bedrooms, bathrooms, car_spaces) VALUES (?, ?)",
              (property_type, bedrooms, bathrooms, car_spaces))
    conn.commit()
    conn.close()


def addSuburb(suburb_id, suburb, age_0_to_4, age_5_to_19, age_20_to_39, age_40_to_59, age_60_plus, postcode, state,
              properties_sold, clearance_rate, median_sale, total_sale):
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO suburbs (suburb_id, suburb, age_0_to_4, age_5_to_19, age_20_to_39, age_40_to_59, age_60_plus, "
        "postcode, state, properties_sold, clearance_rate, median_sale, total_sale) VALUES (?, ?)",
        (suburb_id, suburb, age_0_to_4, age_5_to_19, age_20_to_39, age_40_to_59, age_60_plus, postcode, state,
         properties_sold, clearance_rate, median_sale, total_sale))
    conn.commit()
    conn.close()
