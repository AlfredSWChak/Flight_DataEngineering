import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

connection = sqlite3.connect('flights_database.db', check_same_thread=False)
cursor = connection.cursor()

def getMonth(season):
    
    if season == 'Spring (March, April, May)':
        result = [3,4,5]
    elif season == 'Summer (June, July, August)':
        result = [6,7,8]
    elif season == 'Autumn (September, October, November)':
        result = [9,10,11]
    elif season == 'Winter (December, Janurary, Feburary)':
        result = [12,1,2]
    # elif season == 'Whole year':
    #     result = list(range(1,13))
    
    return result

def hourlyAverage(airport, month_list):
    query = f'SELECT origin, hour, wind_speed, wind_gust, precip, visib FROM weather WHERE month IN ({','.join(['?']*len(month_list))})'
    cursor.execute(query, month_list)
    rows = cursor.fetchall()
    weather_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    weather_df = weather_df[weather_df['origin'] == airport]
    weather_df = weather_df.drop(columns = 'origin')
    
    result_df = pd.DataFrame()
    
    for i in range (0, 24):
        hour_weather_df = weather_df[weather_df['hour'] == i]
        
        hour_result = hour_weather_df.mean(axis = 0, skipna = True)
        
        result_df = pd.concat([result_df, hour_result], axis=1, ignore_index=True)
        
    result_df = result_df.transpose()
    seasonal_result_df = result_df.mean(axis = 0)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=result_df['hour'], y=result_df['wind_speed'], name='Wind Speed',
                         line=dict(color='blue', width=2, dash='dot'), mode='lines+markers'))
    fig.add_trace(go.Scatter(x=result_df['hour'], y=result_df['wind_gust'], name='Wind Gust',
                         line=dict(color='red', width=2, dash='dot'), mode='lines+markers'))
    fig.add_trace(go.Scatter(x=result_df['hour'], y=result_df['visib'], name='Visib',
                         line=dict(color='green', width=2, dash='dot'), mode='lines+markers'))
    fig.update_layout(title=f'Weather information in each hour in {airport}')
    fig.update_layout(plot_bgcolor='white')
    
    return fig, seasonal_result_df

def getTimeHour_df(origin, time_hour_list):
    
    query = f'SELECT * FROM weather WHERE time_hour IN ({','.join(['?']*len(time_hour_list))})'
    cursor.execute(query, time_hour_list)
    rows = cursor.fetchall()
    timeHour_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    timeHour_df = timeHour_df[timeHour_df['origin'] == origin]
    
    return timeHour_df

def count_direction(flights_df):
    
    angle_list = flights_df['angleBetween']
    direction_list = []
    
    for angle in angle_list:
        if angle >= 315 or (angle >=0 and angle <= 45) or (angle <= 0 and angle >= -45) or (angle >= -360 and angle <= -315):
            direction_list.append('Same')
        elif (angle >= 225 and angle <= 315) or (angle <= -45 and angle >= -135):
            direction_list.append('Right')
        elif (angle >= 135 and angle <= 225) or (angle <= -135 and angle >= -225):
            direction_list.append('Opposite')
        elif (angle >= 45 and angle <= 135) or (angle <= -225 and angle >= -315):
            direction_list.append('Left')
        else:
            direction_list.append(None)
    
    flights_df['direction'] = direction_list
    
    return flights_df
    