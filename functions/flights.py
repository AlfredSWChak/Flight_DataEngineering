import sqlite3
import math
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import seaborn as sns
import calendar

connection = sqlite3.connect('flights_database.db')
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