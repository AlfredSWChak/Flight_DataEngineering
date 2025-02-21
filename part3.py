import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
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
    
    query = f'SELECT tailnum, type, manufacturer, model, engines, seats, engine FROM planes WHERE tailnum IN ({','.join(['?']*len(keys))})'
    cursor.execute(query, keys)
    rows = cursor.fetchall()
    planes_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    uniqueTypes_df = planes_df.drop_duplicates(subset=['type', 'manufacturer','model', 'engines', 'seats', 'engine'])
    
    numFlightsList = []
    typePlanes = []

    for i in range(len(uniquePlanes_df)):
        numFlights = list(flights_df['tailnum']).count(uniquePlanes_df.iloc[i]['tailnum'])
        numFlightsList.append(numFlights)
    
    uniquePlanes_df = uniquePlanes_df.assign(numberFlights = numFlightsList)
    
    numPlanesList = []
    
    for i in range(len(uniqueTypes_df)):  
        counter = 0
        this = list(uniqueTypes_df.iloc[i])
        this.pop(0)
    
        for j in range(len(uniquePlanes_df)):
            this_tailnum = uniquePlanes_df.iloc[j]['tailnum']
            
            for k in range(len(planes_df)):
                if (planes_df.iloc[k]['tailnum'] == this_tailnum):
                    plane_row = list(planes_df.iloc[k])
                    plane_row.pop(0)
                    
                    if (this == plane_row):
                        counter = counter + uniquePlanes_df.iloc[j]['numberFlights']
                        break
            
        numPlanesList.append(counter)
    
    uniqueTypes_df = uniqueTypes_df.assign(flights = numPlanesList)
    uniqueTypes_df.drop(columns = 'tailnum', axis=1, inplace=True)
    
    print('There are '+str(len(uniqueTypes_df))+' plane types and '+ str(uniqueTypes_df['flights'].sum())+' flights were used from '+origin+' to '+dest+'. Details are shown below:')
    print(uniqueTypes_df)
        
    return

#  Impossible to run, too slow, should be revised
def topFiveManufacturers(dest):
    
    query = f'SELECT tailnum, origin, dest FROM flights WHERE dest = ?'
    cursor.execute(query, (dest,))
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    uniquePlanes_df = flights_df.drop_duplicates(subset=['tailnum'])
    keys = list(uniquePlanes_df['tailnum'])
    
    query = f'SELECT tailnum, type, manufacturer, model, engines, seats, engine FROM planes WHERE tailnum IN ({','.join(['?']*len(keys))})'
    cursor.execute(query, keys)
    rows = cursor.fetchall()
    planes_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    uniqueTypes_df = planes_df.drop_duplicates(subset=['type', 'manufacturer','model', 'engines', 'seats', 'engine'])
    
    numFlightsList = []
    typePlanes = []

    for i in range(len(uniquePlanes_df)):
        counter = 0
        this_tailnum = uniquePlanes_df.iloc[i]['tailnum']
        
        for j in range(len(flights_df)):
            temp_tailnum = flights_df.iloc[j]['tailnum']
            if(this_tailnum == temp_tailnum):
                counter = counter + 1
        
        numFlightsList.append(counter)
    
    uniquePlanes_df = uniquePlanes_df.assign(numberFlights = numFlightsList)
    
    numPlanesList = []
    
    for i in range(len(uniqueTypes_df)):  
        counter = 0
        this = list(uniqueTypes_df.iloc[i])
        this.pop(0)
    
        for j in range(len(uniquePlanes_df)):
            this_tailnum = uniquePlanes_df.iloc[j]['tailnum']
            
            for k in range(len(planes_df)):
                if(planes_df.iloc[k]['tailnum'] == this_tailnum):
                    plane_row = list(planes_df.iloc[k])
                    plane_row.pop(0)
                    
                    if (this == plane_row):
                        counter = counter + uniquePlanes_df.iloc[j]['numberFlights']
                        break
            
        numPlanesList.append(counter)
    
    uniqueTypes_df = uniqueTypes_df.assign(flights = numPlanesList)
    uniqueTypes_df.drop(columns = 'tailnum', axis=1, inplace=True)
    uniqueTypes_df.sort_values(by = 'flights', ascending=False)
    
    print(uniqueTypes_df.head())
    
    return

def departureDelayPlot():
    
    query = f'SELECT dep_delay, carrier FROM flights'
    cursor.execute(query)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    query = f'SELECT * FROM airlines'
    cursor.execute(query)
    rows = cursor.fetchall()
    airlines_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    avgDelayList = []
    
    for i in range(len(airlines_df)):
        new_df = df[df["carrier"] == airlines_df['carrier'][i]]
        new_df = new_df.dropna(subset=['dep_delay'])
        
        avg_delay = np.average(list(new_df['dep_delay']))
        
        avgDelayList.append(avg_delay)
        
    airlines_df = airlines_df.assign(avg_delay = avgDelayList)
    
    plt.rcParams['figure.figsize'] = [12, 8]
    plt.rcParams["axes.titlesize"] = 20
    plt.rcParams["axes.labelsize"] = 12
    plt.rcParams["xtick.labelsize"] = 6
    plt.title('Average departure delay per flight for each of the airlines')
    sns.barplot(airlines_df, x = 'name', y = 'avg_delay', hue='avg_delay')
    plt.xlabel('Airlines names')
    plt.xticks(rotation=45)
    plt.ylabel('Departure Delay Time')
    plt.show()
    
    return

def arrivalDelayPlot():
    
    query = f'SELECT arr_delay, distance FROM flights'
    cursor.execute(query)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    plt.figure(figsize=(10, 6))
    plt.title('The relationship between the distance of a flight and the arrival delay time')
    sns.scatterplot(df, x='distance', y='arr_delay', size='arr_delay', sizes=(1, 100), hue='arr_delay')
    plt.xlabel('Distances')
    plt.ylabel('Arrival Delay Time')
    plt.show()
    
    plt.figure(figsize=(10, 6))
    plt.title('Distribution of the arrival delay time')
    sns.histplot(data = df['arr_delay'])
    plt.xlabel('Arrival Delay Time')
    plt.ylabel('Frequency')
    plt.show()
    
    return

def amongOfDelayFlights(start_month, end_month, dest):
    
    query = f'SELECT dep_delay, arr_delay, dest FROM flights WHERE month >= ? AND month <= ? AND dest = ?'
    cursor.execute(query, [start_month, end_month, dest])
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    df = df.dropna(subset=['dep_delay','arr_delay'], how='all')
    
    print('For destination',dest,'during month',start_month,'to',end_month,', the amount of delay flights is',len(df),'.')
    
    return