import sqlite3
import pandas as pd
import part1 as pt1

connection = sqlite3.connect('flights_database.db')
cursor = connection.cursor()

# There are five tables: {airlines, airports, flights, planes, weather}
def getTable(input):
    
    tableName = str(input)
    query = f'SELECT * FROM [{tableName}]'
    cursor.execute(query)
    return
    
def getTable_Equal(table, column, faa):
    
    columnName = str(column)
    tableName = str(table)
    query = f'SELECT * FROM [{tableName}] WHERE [{columnName}] = ?'
    cursor.execute(query, (faa,))
    return
                   
def getTable_Larger(table, column, value):
    
    columnName = str(column)
    tableName = str(table)
    query = f'SELECT * FROM [{tableName}] WHERE [{columnName}] > ?'
    cursor.execute(query, (value,))
    return
    
def getTable_Smaller(table, column, value):
    
    columnName = str(column)
    tableName = str(table)
    query = f'SELECT * FROM [{tableName}] WHERE [{columnName}] < ?'
    cursor.execute(query, (value,))
    return

def printTable():
    rows = cursor.fetchall()
    all = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])

    print(all)
    return
    
def fetch_table_data(table_name):

    cursor.execute('select * from ' + table_name)
    header = [row[0] for row in cursor.description]
    rows = cursor.fetchall()

    return header, rows

def export(table_name):
    
    header, rows = fetch_table_data(table_name)
    
    # Create csv file
    file = open(table_name + '.csv', 'w')
    # Write header
    file.write(','.join(header) + '\n')
    
    for row in rows:
        file.write(','.join(str(r) for r in row) + '\n')
        
    file.close()
    print(str(len(rows)) + ' rows written successfully to ' + file.name)
    return
    
def showAllTableNames():
    query = f"SELECT name FROM sqlite_master WHERE type='table';"
    cursor.execute(query)
    
    print(cursor.fetchall())
    return
    
def printFlightsOnDateAtAirport(month, day, airport):
    
    query = f'SELECT month, day, origin, dest FROM flights WHERE month = ? AND day = ? AND origin = ?'
    cursor.execute(query, [month, day, airport])
    
    rows = cursor.fetchall()
    new_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
        
    destinationList = new_df['dest']
    
    pt1.drawMultipleLines(destinationList, month, day, airport)
    
    return

def printStatisticsOnDateAtAirport(month, day, airport):
    
    query = f'SELECT month, day, origin, dest FROM flights WHERE month = ? AND day = ? AND origin = ?'
    cursor.execute(query, [month, day, airport])
    
    rows = cursor.fetchall()
    new_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
        
    numFlights = len(new_df)

    uniqueDest_df = new_df.drop_duplicates(subset=['dest'])
    numUniqueDest = len(uniqueDest_df)
    
    numMost = 0
    
    for i in range(len(uniqueDest_df)):
        counter = 0
        
        # print(uniqueDest_df.iloc[i]['dest'])
        
        for j in range(len(new_df)):
            if (uniqueDest_df.iloc[i]['dest'] == new_df.iloc[j]['dest']):
                counter = counter + 1
                
        if (counter > numMost):
            destMost = uniqueDest_df.iloc[i]['dest']
            numMost = counter
    
    print('On '+str(day)+'/'+str(month)+' at '+airport+', there are '+str(numFlights)+' flights.')
    print('On '+str(day)+'/'+str(month)+' at '+airport+', there are '+str(numUniqueDest)+' unique destinations.')
    print('On '+str(day)+'/'+str(month)+' at '+airport+', '+destMost+' is visited most often with '+str(numMost)+' flights.')
    
    return

def printPlanesStatistics(origin, dest):
    
    query = f'SELECT tailnum, origin, dest FROM flights WHERE origin = ? AND dest = ?'
    cursor.execute(query, [origin, dest])
    
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    uniquePlanes_df = flights_df.drop_duplicates(subset=['tailnum'])
    keys = list(uniquePlanes_df['tailnum'])
    
    numFlightsList = []
    typePlanes = []

    for i in range(len(uniquePlanes_df)):
        counter = 0
        
        for j in range(len(flights_df)):
            if(uniquePlanes_df.iloc[i]['tailnum'] == flights_df.iloc[j]['tailnum']):
                counter = counter + 1
        
        numFlightsList.append(counter)
    
    uniquePlanes_df = uniquePlanes_df.assign(numberFlights = numFlightsList)

    query = f'SELECT tailnum, type, manufacturer, model, engines, seats, engine FROM planes WHERE tailnum IN ({','.join(['?']*len(keys))})'
    cursor.execute(query, keys)
    
    rows = cursor.fetchall()
    planes_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    uniqueTypes_df = planes_df.drop_duplicates(subset=['type', 'manufacturer','model', 'engines', 'seats', 'engine'])
        
    return

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
    print("Planes table updated with average speeds.")

planes_speed()
export("planes")