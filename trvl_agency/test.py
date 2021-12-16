import sqlite3

connection = sqlite3.connect('Travel_Agency.db')
cur = connection.cursor()

cur.execute("INSERT INTO Location(COUNTRY_NAME,S_DATE,E_DATE,PRICE) VALUES ('Canada', '2021-05-05', '2021-09-22', '1200')")
cur.execute("INSERT INTO Location(COUNTRY_NAME,S_DATE,E_DATE,PRICE) VALUES ('USA', '2021-11-18', '2021-12-22', '1300')")
cur.execute("INSERT INTO Location(COUNTRY_NAME,S_DATE,E_DATE,PRICE) VALUES ('Brazil', '2021-03-25', '2021-05-19', '1400')")

connection.commit()
connection.close()
