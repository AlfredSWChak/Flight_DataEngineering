import sqlite3
import pandas as pd
import seaborn as sns

connection = sqlite3.connect('flights_database.db')
cursor = connection.cursor()

def top_five_planes():
    
    query = f'SELECT * FROM planes'
    cursor.execute(query)
    rows = cursor.fetchall()
    planes_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])

    unique_planes_df = planes_df.drop_duplicates(subset=['manufacturer', 'model'])
    
    count_planes_df = planes_df.groupby(by=['manufacturer', 'model']).size().reset_index(name='numPlanes')
    top_five = count_planes_df.sort_values(by=['numPlanes'], ascending=False).head()
    
    result = pd.DataFrame()
    
    for manufacturer, model, numPlanes in zip(top_five['manufacturer'], top_five['model'], top_five['numPlanes']):
        result = pd.concat([result, unique_planes_df[(unique_planes_df['manufacturer'] == manufacturer) & (unique_planes_df['model'] == model)]])
        
    result = result.assign(numPlanes=list(top_five['numPlanes']))
    result = result.drop(columns=['tailnum', 'year'])
    
    # print(result.to_string(index=False))
    
    return result

def top_five_flights(airport):
    
    if(airport == 'All airports'):
        query = f'SELECT origin, dest, distance FROM flights'
        cursor.execute(query)
    else:
        query = f'SELECT origin, dest, distance FROM flights WHERE origin = ?'
        cursor.execute(query, (airport,))
    
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    unique_flights_df = flights_df.drop_duplicates(subset=['origin', 'dest'])
    
    count_flights_df = flights_df.groupby(by=['origin', 'dest']).size().reset_index(name='numFlights')
    top_five = count_flights_df.sort_values(by=['numFlights'], ascending=False).head()
    
    result = pd.DataFrame()
    
    for origin, dest, numFlights in zip(top_five['origin'], top_five['dest'], top_five['numFlights']):
        result = pd.concat([result, unique_flights_df[(unique_flights_df['origin'] == origin) & (unique_flights_df['dest'] == dest)]])
    
    result = result.assign(numFlights=list(top_five['numFlights']))
    result = result.astype({'distance':'int'})
    
    return result

