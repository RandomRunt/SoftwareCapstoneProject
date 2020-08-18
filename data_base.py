import sqlite3


def createTable():
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE property_ids(property_id text, address text, qty integer, price real, coordinate text, 
    domain_id text)''')
    conn.commit()
    conn.close()