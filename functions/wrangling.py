import sqlite3
import pandas as pd

connection = sqlite3.connect('flights_database.db', check_same_thread=False)
cursor = connection.cursor()

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