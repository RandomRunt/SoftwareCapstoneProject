import sqlite3


def createTable():
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE property_ids(property_id text, address text, qty integer, price real)''')

    Address
    Price
    Coordinate
    domain_id

    conn.commit()
    conn.close()