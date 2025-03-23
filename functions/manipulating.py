import sqlite3
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import functions.extra as ex

connection = sqlite3.connect('flights_database.db', check_same_thread=False)
cursor = connection.cursor()

# There are five tables: {airlines, airports, flights, planes, weather}
def getTable(input):
    
    tableName = str(input)
    query = f'SELECT * FROM [{tableName}]'
    cursor.execute(query)
    rows = cursor.fetchall()
    all = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    return all
    
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
    
    query = f'SELECT month, day, carrier, origin, dest, distance FROM flights WHERE month = ? AND day = ? AND origin = ?'
    cursor.execute(query, [month, day, airport])
    rows = cursor.fetchall()
    new_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
        
    destinationList = new_df['dest']
    
    result = ex.drawMultipleLines(destinationList, month, day, airport)
    
    return result

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
        
        
        for j in range(len(new_df)):
            if (uniqueDest_df.iloc[i]['dest'] == new_df.iloc[j]['dest']):
                counter = counter + 1
                
        if (counter > numMost):
            destMost = uniqueDest_df.iloc[i]['dest']
            numMost = counter
    
    return numFlights, numUniqueDest, destMost, numMost

def unique_depart_airports():
    
    query = f'SELECT origin FROM flights'
    cursor.execute(query)
    rows = cursor.fetchall()
    origin_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    origin_df_list = origin_df.drop_duplicates()['origin'].tolist()
    
    query = f'SELECT * FROM airports WHERE faa IN ({','.join(['?']*len(origin_df_list))})'
    cursor.execute(query, origin_df_list)
    rows = cursor.fetchall()
    airports_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    return

def unique_depart_airports_input(dest):
    
    query = f'SELECT origin FROM flights WHERE dest = ?'
    cursor.execute(query, (dest,))
    rows = cursor.fetchall()
    origin_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    origin_df_list = origin_df.drop_duplicates()['origin'].tolist()

    return origin_df_list

def unique_arrive_airports():
    
    query = f'SELECT dest FROM flights'
    cursor.execute(query)
    rows = cursor.fetchall()
    dest_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    dest_df_list = dest_df.drop_duplicates()['dest'].tolist()
    
    query = f'SELECT * FROM airports WHERE faa IN ({','.join(['?']*len(dest_df_list))})'
    cursor.execute(query, dest_df_list)
    rows = cursor.fetchall()
    airports_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    return dest_df_list

def unique_arrive_airports_input(origin):
    
    query = f'SELECT dest FROM flights WHERE origin = ?'
    cursor.execute(query, (origin,))
    rows = cursor.fetchall()
    dest_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    dest_df_list = dest_df.drop_duplicates()['dest'].tolist()
    
    query = f'SELECT * FROM airports WHERE faa IN ({','.join(['?']*len(dest_df_list))})'
    cursor.execute(query, dest_df_list)
    rows = cursor.fetchall()
    airports_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    return dest_df_list