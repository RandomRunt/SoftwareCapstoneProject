import sqlite3

def createTable():
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE property_ids(property_id text, address text, price integer, coordinate text, 
    domain_id text)''')
    c.execute('''CREATE TABLE property_features(property_type text, bedrooms integer, bathrooms integer, car_spaces 
    integer, )''')
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
