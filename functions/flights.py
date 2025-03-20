import sqlite3
import math
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import seaborn as sns
import calendar
from datetime import datetime
import functions.weather as wthr
import alfred_function as af

connection = sqlite3.connect('flights_database.db', check_same_thread=False)
cursor = connection.cursor()

def averageDelay(origin,dest):
    
    query = f'SELECT dep_delay, arr_delay, origin, dest FROM flights WHERE origin = ? AND dest = ?'
    cursor.execute(query, (origin, dest,))
    rows = cursor.fetchall()
    delay_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    avg_dep_delay = round(delay_df['dep_delay'].mean(),3)
    avg_arr_delay = round(delay_df['arr_delay'].mean(),3)
    
    return avg_dep_delay, avg_arr_delay 

def flightsPerMonth(origin,dest):
    
    query = f'SELECT month, origin, dest FROM flights WHERE origin = ? AND dest = ?'
    cursor.execute(query, (origin, dest,))
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    result = 0
    
    for i in range(1,13):
        month_flights_df = flights_df[flights_df['month'] == i]
        numFlights = len(month_flights_df)
        result = result + numFlights / 12
    
    result = round(result,3)
    
    return result

def flightsPerDay(origin,dest):
    
    query = f'SELECT month, day, origin, dest FROM flights WHERE origin = ? AND dest = ?'
    cursor.execute(query, (origin, dest,))
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    result = 0
    
    for i in range(1,13):
        month_flights_df = flights_df[flights_df['month'] == i]
        numDay = calendar.monthrange(2023, i)[1]
        numFlights = len(month_flights_df)
        result = result + numFlights / numDay / 12
    
    result = round(result,3)
    
    return result

def delayDotProduct(start_month, end_month, origin, dest):
    
    query = f'SELECT dep_delay, origin, dest, tailnum, time_hour FROM flights WHERE origin = ? AND dest = ? AND dep_delay > ? AND month >= ? AND month <= ?'
    cursor.execute(query, [origin, dest, 0, start_month, end_month])
    rows = cursor.fetchall()
    delay_flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    dest_direction = af.getAngleBetween(origin, dest)
    if (dest_direction < 0):
        dest_direction = 360 + dest_direction
    
    temp = delay_flights_df.copy().drop_duplicates(subset=['time_hour'])
    time_hour_list = delay_flights_df['time_hour'].tolist()
    delay_weather_df = wthr.getTimeHour_df(origin, time_hour_list)
    
    temp = delay_flights_df.copy().drop_duplicates(subset=['tailnum'])
    tailnum_list = delay_flights_df['tailnum'].tolist()   
    planes_df = af.getTailnumPlanes(tailnum_list)
    
    dot_product_list = []
    angle_list = []
        
    for time_hour, tailnum in zip(delay_flights_df['time_hour'], delay_flights_df['tailnum']):
        
        if (time_hour in delay_weather_df['time_hour'].tolist()) and (tailnum in planes_df['tailnum'].tolist()):    
            wind_direction_weather = delay_weather_df[delay_weather_df['time_hour'] == time_hour]['wind_dir'].iloc[0]
            wind_speed_weather = delay_weather_df[delay_weather_df['time_hour'] == time_hour]['wind_speed'].iloc[0]
            angle = abs(dest_direction - wind_direction_weather)    
            magnitude = planes_df[planes_df['tailnum'] == tailnum]['speed'].iloc[0]
            dot_product = abs(magnitude) * abs(wind_speed_weather) * math.cos(math.radians(angle))
        
            angle_list.append(angle)
            dot_product_list.append(dot_product)
        else:
            angle_list.append(0)
            dot_product_list.append(0)
        
    new_delay_flights_df = delay_flights_df.assign(angleBetween = angle_list)
    new_delay_flights_df = new_delay_flights_df.assign(dotProduct = dot_product_list)
    
    fig = px.scatter_polar(new_delay_flights_df, r='dotProduct', theta='angleBetween')
    
    return fig, dest_direction, new_delay_flights_df