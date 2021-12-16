import sqlite3 as sql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot

conn = sql.connect('trvlag.db')

query = '''SELECT * FROM booking'''

df = pd.read_sql_query(query, conn)
print(df.head())

listCountry0 = df['COUNTRY_NAME'] == df['COUNTRY_NAME'][0]
listCountry1  = df['COUNTRY_NAME'] == df['COUNTRY_NAME'][1]
listCountry2 = df['COUNTRY_NAME'] == df['COUNTRY_NAME'][3]

data = {str(df['COUNTRY_NAME'][0]): len(df[listCountry0]),
         str(df['COUNTRY_NAME'][1]): len(df[listCountry1]),
         str(df['COUNTRY_NAME'][3]): len(df[listCountry2]) }

courses = list(data.keys())
values = list(data.values())

fig = plot.figure(figsize = (8, 4))
plot.bar(courses, values, color ='blue', width = 0.5)
plot.xlabel("Country")
plot.ylabel("Count")
plot.title("No of entries in the country")
plot.show()