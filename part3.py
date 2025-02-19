import sqlite3
import pandas as pd

connection = sqlite3.connect('flights_database.db')

query = f'SELECT * FROM flights'

cursor = connection.cursor()
cursor.execute(query)

rows = cursor.fetchall()
whole = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])

print (whole)