import sqlite3


def about_queries(name,email,subject,message):  # James Lu
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    c.execute("INSERT INTO about_queries (name,email,subject,message) VALUES (?, ?, ?, ?)"
              , (name,email,subject,message))
    conn.commit()
    conn.close()


def get_about_queries():  # James Lu
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    names = []
    emails = []
    subjects = []
    messages = []
    length = 0
    c.execute('SELECT * FROM about_queries')
    for row in c:
        length += 1
        names.append(row[0])
        emails.append(row[1])
        subjects.append(row[2])
        messages.append(row[3])
    return(names, emails, subjects, messages, length)
    conn.close()


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
                image, lat_coordinate, long_coordinate, property_type, bedrooms, bathrooms, car_spaces, areaSize,
                postcode):
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    c.execute("INSERT INTO properties_data_base (property_id, street_name, street_num, suburb, street_type, state, "
              "lower_price, upper_price, mid_price, image, lat_coordinate, long_coordinate, property_type, bedrooms, "
              "bathrooms, car_spaces, areaSize, postcode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
              , (property_id, street_name, street_num, suburb, street_type, state, lower_price, upper_price, mid_price,
                 image, lat_coordinate, long_coordinate, property_type, bedrooms, bathrooms, car_spaces, areaSize,
                 postcode))

    conn.commit()
    conn.close()


def addSuburb(suburb_id, suburb, age_0_to_4, age_5_to_19, age_20_to_39, age_40_to_59, age_60_plus, postcode,
                      state, population, median_sold_price_2018, number_sold_2018, highest_sold_price_2018,
                      lowest_sold_price_2018, percentile_sold_price_5_2018, percentile_sold_price_25_2018,
                      percentile_sold_price_75_2018, percentile_sold_price_95_2018, median_sold_price_2019,
                      number_sold_2019, highest_sold_price_2019, lowest_sold_price_2019,
                      percentile_sold_price_5_2019, percentile_sold_price_25_2019, percentile_sold_price_75_2019,
                      percentile_sold_price_95_2019, median_sold_price_2020, number_sold_2020, highest_sold_price_2020,
                      lowest_sold_price_2020, percentile_sold_price_5_2020, percentile_sold_price_25_2020,
                      percentile_sold_price_75_2020, percentile_sold_price_95_2020):
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    c.execute("INSERT INTO suburbs (suburb_id, suburb, age_0_to_4, age_5_to_19, age_20_to_39, age_40_to_59, "
              "age_60_plus, postcode, state, population, median_sold_price_2018, number_sold_2018, "
              "highest_sold_price_2018, lowest_sold_price_2018, percentile_sold_price_5_2018, "
              "percentile_sold_price_25_2018, percentile_sold_price_75_2018, percentile_sold_price_95_2018, "
              "median_sold_price_2019, number_sold_2019, highest_sold_price_2019, lowest_sold_price_2019, "
              "percentile_sold_price_5_2019, percentile_sold_price_25_2019, percentile_sold_price_75_2019, "
              "percentile_sold_price_95_2019, median_sold_price_2020, number_sold_2020, highest_sold_price_2020, "
              "lowest_sold_price_2020, percentile_sold_price_5_2020, percentile_sold_price_25_2020, "
              "percentile_sold_price_75_2020, percentile_sold_price_95_2020) VALUES (?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,"
              "?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (suburb_id, suburb, age_0_to_4, age_5_to_19, age_20_to_39, age_40_to_59, age_60_plus, postcode, state,
         population, median_sold_price_2018, number_sold_2018, highest_sold_price_2018, lowest_sold_price_2018,
         percentile_sold_price_5_2018, percentile_sold_price_25_2018, percentile_sold_price_75_2018,
         percentile_sold_price_95_2018, median_sold_price_2019, number_sold_2019, highest_sold_price_2019,
         lowest_sold_price_2019,percentile_sold_price_5_2019, percentile_sold_price_25_2019,
         percentile_sold_price_75_2019, percentile_sold_price_95_2019, median_sold_price_2020, number_sold_2020,
         highest_sold_price_2020, lowest_sold_price_2020, percentile_sold_price_5_2020, percentile_sold_price_25_2020,
         percentile_sold_price_75_2020, percentile_sold_price_95_2020))
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


def checkSuburb():
    conn = sqlite3.connect("properties.db")
    cur  = conn.cursor()
    suburbs = []
    for suburb in cur.execute("SELECT suburb FROM suburbs"):
        suburbs.append(suburb)
    return suburbs
    conn.close()
    


def findProperty(property_id):
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    property = []
    for row in c.execute('SELECT * FROM properties_data_base WHERE property_id=?', (property_id,)):
        property.append(row)
    return property
    conn.close()
