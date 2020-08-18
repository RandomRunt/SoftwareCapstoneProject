import sqlite3


def createTable():
    conn = sqlite3.connect('properties.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE property_ids(property_id text, address text, price real, coordinate text, 
    domain_id text)''')
    conn.commit()
    conn.close()


def addProperty(property_id, address, ):
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (fName, sName) VALUES (?, ?)", (fname, sname))
    conn.commit()
    conn.close()
