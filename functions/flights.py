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
import functions.extra as ex

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

def getNonDelayFlight(start_month, end_month, origin, dest):
    
    query = f'SELECT * FROM flights WHERE origin = ? AND dest = ? AND dep_delay <= ? AND month >= ? AND month <= ?'
    cursor.execute(query, [origin, dest, 0, start_month, end_month])
    rows = cursor.fetchall()
    non_delay_flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    return non_delay_flights_df

def nonDelayDotProduct(start_month, end_month, origin, dest):
    query = f'SELECT dep_delay, origin, dest, tailnum, time_hour FROM flights WHERE origin = ? AND dest = ? AND dep_delay <= ? AND month >= ? AND month <= ?'
    cursor.execute(query, [origin, dest, 0, start_month, end_month])
    rows = cursor.fetchall()
    delay_flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    dest_direction = ex.getAngleBetween(origin, dest)
    if (dest_direction < 0):
        dest_direction = 360 + dest_direction
    
    temp = delay_flights_df.copy().drop_duplicates(subset=['time_hour'])
    time_hour_list = delay_flights_df['time_hour'].tolist()
    delay_weather_df = wthr.getTimeHour_df(origin, time_hour_list)
    
    temp = delay_flights_df.copy().drop_duplicates(subset=['tailnum'])
    tailnum_list = delay_flights_df['tailnum'].tolist()   
    planes_df = ex.getTailnumPlanes(tailnum_list)
    
    dot_product_list = []
    angle_list = []
        
    for time_hour, tailnum in zip(delay_flights_df['time_hour'], delay_flights_df['tailnum']):
        
        if (time_hour in delay_weather_df['time_hour'].tolist()) and (tailnum in planes_df['tailnum'].tolist()):    
            wind_direction_weather = delay_weather_df[delay_weather_df['time_hour'] == time_hour]['wind_dir'].iloc[0]
            wind_speed_weather = delay_weather_df[delay_weather_df['time_hour'] == time_hour]['wind_speed'].iloc[0]
            angle = dest_direction - wind_direction_weather   
            magnitude = planes_df[planes_df['tailnum'] == tailnum]['speed'].iloc[0]
            dot_product = abs(magnitude) * abs(wind_speed_weather) * math.cos(math.radians(abs(angle)))
        
            angle_list.append(angle)
            dot_product_list.append(abs(dot_product))
        else:
            angle_list.append(0)
            dot_product_list.append(0)
        
    new_delay_flights_df = delay_flights_df.assign(angleBetween = angle_list)
    new_delay_flights_df = new_delay_flights_df.assign(dotProduct = dot_product_list)
    
    return new_delay_flights_df

def delayDotProduct(start_month, end_month, origin, dest):
    
    query = f'SELECT dep_delay, origin, dest, tailnum, time_hour FROM flights WHERE origin = ? AND dest = ? AND dep_delay > ? AND month >= ? AND month <= ?'
    cursor.execute(query, [origin, dest, 0, start_month, end_month])
    rows = cursor.fetchall()
    delay_flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    dest_direction = ex.getAngleBetween(origin, dest)
    if (dest_direction < 0):
        dest_direction = 360 + dest_direction
    
    temp = delay_flights_df.copy().drop_duplicates(subset=['time_hour'])
    time_hour_list = delay_flights_df['time_hour'].tolist()
    delay_weather_df = wthr.getTimeHour_df(origin, time_hour_list)
    
    temp = delay_flights_df.copy().drop_duplicates(subset=['tailnum'])
    tailnum_list = delay_flights_df['tailnum'].tolist()   
    planes_df = ex.getTailnumPlanes(tailnum_list)
    
    dot_product_list = []
    angle_list = []
        
    for time_hour, tailnum in zip(delay_flights_df['time_hour'], delay_flights_df['tailnum']):
        
        if (time_hour in delay_weather_df['time_hour'].tolist()) and (tailnum in planes_df['tailnum'].tolist()):    
            wind_direction_weather = delay_weather_df[delay_weather_df['time_hour'] == time_hour]['wind_dir'].iloc[0]
            wind_speed_weather = delay_weather_df[delay_weather_df['time_hour'] == time_hour]['wind_speed'].iloc[0]
            angle = dest_direction - wind_direction_weather   
            magnitude = planes_df[planes_df['tailnum'] == tailnum]['speed'].iloc[0]
            dot_product = abs(magnitude) * abs(wind_speed_weather) * math.cos(math.radians(abs(angle)))
        
            angle_list.append(angle)
            dot_product_list.append(abs(dot_product))
        else:
            angle_list.append(0)
            dot_product_list.append(0)
        
    new_delay_flights_df = delay_flights_df.assign(angleBetween = angle_list)
    new_delay_flights_df = new_delay_flights_df.assign(dotProduct = dot_product_list)
        
    wind_fig = px.scatter_polar()
    wind_fig.add_scatterpolar(r=new_delay_flights_df['dotProduct'], theta=new_delay_flights_df['angleBetween'], mode='markers', marker_color='red')
    # nonDelay_df = nonDelayDotProduct(start_month, end_month, origin, dest)
    # wind_fig.add_scatterpolar(r=nonDelay_df['dotProduct'], theta=nonDelay_df['angleBetween'], mode='markers', marker_color='green')
    
    new_time_hour_list = getNonDelayFlight(start_month, end_month, origin, dest)['time_hour'].tolist()
    
    non_delay_weather_df = wthr.getTimeHour_df(origin, new_time_hour_list)
    non_delay_weather_visib_list = non_delay_weather_df['visib'].tolist()
    
    num_delay = len(new_delay_flights_df)
    num_non_delay = len(new_time_hour_list)

    visib_fig = go.Figure()
    visib_fig.add_trace(go.Histogram(x=delay_weather_df['visib'], marker_color='rgb(26, 118, 255)', name='Delay'))
    visib_fig.add_trace(go.Histogram(x=non_delay_weather_visib_list, marker_color='rgb(55, 83, 109)', name='Non-Delay'))
    visib_fig.update_layout(bargap=0.2, bargroupgap=0.1)
    
    direction_fig = wthr.count_direction(new_delay_flights_df)
    
    wind_fig.update_layout(title = f'Angle between flight direction and wind direction of delay flights')
    visib_fig.update_layout(title = f'Visibility of all the flights ')
    
    return wind_fig, visib_fig, dest_direction, num_delay, num_non_delay, direction_fig

def get_all_destinations(origin):
    query = f"SELECT DISTINCT dest FROM flights WHERE origin = ?"
    cursor.execute(query, (origin,))
    rows = cursor.fetchall()

    destinations = [row[0] for row in rows]
    return destinations

def get_flight_data():
    query = "SELECT * FROM flights"
    cursor.execute(query)
    rows = cursor.fetchall()

    flights_df = pd.DataFrame(rows, columns=[x[0] for x in cursor.description])
    return flights_df

def flightsPerMonthByOrigin(origin):
    query = 'SELECT month, COUNT(*) FROM flights WHERE origin = ? GROUP BY month ORDER BY month'
    cursor.execute(query, (origin,))
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns=['month', 'num_flights'])
    return flights_df

def totalDelayPerMonthByOrigin(origin):
    query = 'SELECT month, SUM(dep_delay + arr_delay) FROM flights WHERE origin = ? GROUP BY month ORDER BY month'
    cursor.execute(query, (origin,))
    rows = cursor.fetchall()
    delay_df = pd.DataFrame(rows, columns=['month', 'total_delay'])
    return delay_df

def get_all_destinations(origin):
    query = "SELECT DISTINCT dest FROM flights WHERE origin = ?"
    cursor.execute(query, (origin,))
    rows = cursor.fetchall()

    destinations = [row[0] for row in rows]
    return destinations

def get_flights_number(origin, dest):
    
    query = f'SELECT month, origin, dest FROM flights WHERE origin = ? AND dest = ?'
    cursor.execute(query, (origin, dest,))
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    count_flights_df = flights_df.groupby(by=['month']).size().reset_index(name='numFlights')
    new_df = pd.DataFrame(columns=['month', 'numFlights'])
    new_df['month'] = list(range(1,13))
    num_list = []
    
    for month, numFlights in zip(new_df['month'], new_df['numFlights']):
        
        if month in count_flights_df['month'].values:
            numFlights = count_flights_df[count_flights_df['month'] == month]['numFlights'].iloc[0]
            
        else:
            numFlights = 0
            
        num_list.append(numFlights)
        
    new_df['numFlights'] = num_list
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=new_df['month'], y=new_df['numFlights'], name='Number of flights',
                         line=dict(color='blue', width=2), mode='lines+markers'))
    fig.update_layout(title=f'Number of flights from {origin} to {dest} in each month',
                      xaxis=dict(title=dict(text='Month'), type='category'),yaxis=dict(title=dict(text='Number of flights')))
    fig.update_layout(plot_bgcolor='white')
    
    return fig