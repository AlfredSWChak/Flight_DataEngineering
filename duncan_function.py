import sqlite3
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import math 

connection = sqlite3.connect('flights_database.db')
cursor = connection.cursor()

def busiest_routes():
    query = f'''SELECT origin , dest, COUNT(*) as num_flights 
    FROM flights
    GROUP BY origin, dest 
    ORDER BY num_flights DESC
    LIMIT 5
    '''

    cursor.execute(query)
    rows = cursor.fetchall()
    routes_df = pd.DataFrame(rows, columns=['origin', 'dest', 'num_flights'])
    return routes_df

def weather_impact_on_delays():
    query = f'''
    SELECT weather.year, weather.month, 
           SUM(flights.dep_delay) AS total_dep_delay,
           SUM(flights.arr_delay) AS total_arr_delay,
           AVG(flights.dep_delay) AS avg_dep_delay,
           AVG(flights.arr_delay) AS avg_arr_delay
    FROM weather
    JOIN flights
    ON weather.origin = flights.origin 
    AND weather.year = flights.year 
    AND weather.month = flights.month 
    AND weather.day = flights.day 
    AND weather.hour = flights.hour
    GROUP BY weather.year, weather.month
    ORDER BY total_dep_delay DESC
    '''

    cursor.execute(query)
    rows = cursor.fetchall()
    weather_delay_df = pd.DataFrame(rows, columns=['origin', 'temp', 'wind_speed', 'precip', 'dep_delay', 'arr_delay'])
    return weather_delay_df
    
routes_df = busiest_routes()
print("Busiest Routes:")
print(routes_df)

weather_delay_df = weather_impact_on_delays()
print("\nWeather Impact on Delays:")
print(weather_delay_df)