import sqlite3
import pandas as pd
from datetime import datetime
import functions.manipulating as mp

connection = sqlite3.connect('flights_database.db', check_same_thread=False)
cursor = connection.cursor()

def check_na_flights():
    
    df = mp.getTable('flights')
    result = pd.DataFrame()
    
    nan_rows = df.isna().any(axis=1)
    
    nan_df = df[df.isna().any(axis=1)]
    
    print(nan_df)
      
    return result

def drop_duplicates_except(except_list):
    
    df = mp.getTable('flights')
    result = pd.DataFrame()
    
    column_list = df.columns.tolist()
    
    for element in except_list:
        column_list.remove(element)
    
    df.drop_duplicates(subset = column_list)
        
    print(df)

    return

def convert_datetime():
    
    query = f'SELECT year, month, day, dep_time, sched_dep_time, arr_time, sched_arr_time FROM flights'
    cursor.execute(query)
    rows = cursor.fetchall()
    new_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    new_df = new_df.dropna()
    
    datetime_list = []
    
    for i in range(len(new_df)):
        row = new_df.iloc[i]
        year = int(row['year'])
        month = int(row['month'])
        day = int(row['day'])
        time = str(int(row['arr_time']))
        
        if (len(time) >= 3):
            hour = int(time[:(len(time)-2)])
            minute = int(time[(len(time)-2):])
            
            if (hour == 24):
                hour = 0
                # day = day + 1
        else:
            hour = 0
            minute = int(time)
        
        this_datetime = datetime(year, month, day, hour, minute)
        
        datetime_list.append(this_datetime)
    
    new_df = new_df.assign(dateTime_arr_time = datetime_list)
    
    print(new_df)
    
    return

def local_arrival_time():
    
    query = f'SELECT arr_time, origin, dest FROM flights'
    cursor.execute(query)
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    query = f'SELECT faa, tz FROM airports'
    cursor.execute(query)
    rows = cursor.fetchall()
    airports_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    flights_df = flights_df.dropna()
    
    arrival_list = []
    
    EWR_tz = 0
    JFK_tz = 0
    LGA_tz = 0
    
    for i in airports_df.index:
        if (airports_df['faa'][i] == 'EWR'):
            EWR_tz =  airports_df['tz'][i]
        elif (airports_df['faa'][i] == 'JFK'):
            JFK_tz =  airports_df['tz'][i]
        elif (airports_df['faa'][i] == 'LGA'):
            LGA_tz =  airports_df['tz'][i]
    
    for i in flights_df.index:
        dest_faa = flights_df['dest'][i]
        origin_faa = flights_df['origin'][i]
        
        dest_tz = 0
        origin_tz = 0
        
        if (origin_faa == 'EWR'):
            origin_tz = EWR_tz
        elif (origin_faa == 'JFK'):
            origin_tz = JFK_tz
        elif (origin_faa == 'LGA'):
            origin_tz = LGA_tz
        
        for j in airports_df.index:
            if (airports_df['faa'][j] == dest_faa):
                dest_tz = airports_df['tz'][j]
                break
        
        arrival_time = flights_df['arr_time'][i] + (dest_tz - origin_tz) * 100
        
        print (flights_df['arr_time'][i], origin_tz, dest_tz, arrival_time)
        
        arrival_list.append(arrival_time) 
    
    print(new_df)
    
    return

def correctAirportsTable():
    
    update_query = f'UPDATE airports SET name = ?, lat = ?, lon = ?, alt = ?, tz = ?, dst = ?, tzone = ? WHERE faa = ?'
    cursor.execute(update_query, ('Terre Haute Regional Airport	(Hulman Field)',39.4515,-87.307602,589,-5,'A','America/New_York', 'HUF'))

    update_query = f'UPDATE airports SET name = ?, lat = ?, lon = ?, alt = ?, tz = ?, dst = ?, tzone = ? WHERE faa = ?'
    cursor.execute(update_query, ('Pine Bluff Regional Airport	(Grider Field)',34.1731,-91.9356,206,-6,'A','America/Chicago', 'PBF'))
    
    connection.commit()
    
    return

# correctAirportsTable()

def planes_speed():
    query_flights = "SELECT tailnum, distance, air_time FROM flights WHERE air_time > 0"
    cursor.execute(query_flights)
    flights_data = cursor.fetchall()

    speed_dict = {}
    for tailnum, distance, air_time in flights_data:
        if tailnum not in speed_dict:
            speed_dict[tailnum] = {"total_distance": 0, "total_time": 0}
            speed_dict[tailnum]["total_distance"] += distance
            speed_dict[tailnum]["total_time"] += air_time

    average_speed = {tailnum: data["total_distance"] / data["total_time"] for tailnum, data in speed_dict.items() if data["total_time"] > 0}

    query_planes = "SELECT tailnum, model FROM planes"
    cursor.execute(query_planes)
    planes_data = cursor.fetchall()

    planemodel_speeds = {}
    planemodel_counts = {}

    for tailnum, model in planes_data:
        if tailnum in average_speed:
            if model not in planemodel_speeds:
                planemodel_speeds[model] = 0
                planemodel_counts[model] = 0
            planemodel_speeds[model] += average_speed[tailnum]
            planemodel_counts[model] += 1
    
    total_speed = {model: planemodel_speeds[model] / planemodel_counts[model] for model in planemodel_speeds}

    update_query = "UPDATE planes SET speed = ? WHERE model = ?"
    for model, average_speed in total_speed.items():
        cursor.execute(update_query, (average_speed, model))

    connection.commit()
    
# planes_speed()