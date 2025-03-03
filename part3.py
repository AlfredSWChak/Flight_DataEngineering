import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import seaborn as sns
import part1 as pt1

connection = sqlite3.connect('flights_database.db')
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
    
    pt1.drawMultipleLines(destinationList, month, day, airport)
    
    print('There are '+str(len(new_df))+' flights departed from '+airport+' airport on '+ str(day)+'/'+str(month)+'.')
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    plt.rcParams["axes.titlesize"] = 12
    plt.rcParams["axes.labelsize"] = 10
    plt.rcParams["xtick.labelsize"] = 6
    
    ax = sns.histplot(data = new_df['distance'], ax=axs[0])
    axs[0].set_title('Distribution of distance')
    axs[0].tick_params(labelsize=6, labelrotation=90)
    axs[0].set_xlabel('distance', fontsize=10)
    axs[0].set_ylabel('frequency', fontsize=10)
    
    for i in ax.containers:
        ax.bar_label(i,fontsize=6)
    
    unique_values = new_df['carrier'].unique()
    unique_counts = []
    
    for value in unique_values:
        counter = 0
        counter = new_df['carrier'].value_counts().get(value, 0)
        unique_counts.append(counter)
    
    plot_df = pd.DataFrame({'name': unique_values, 'frequency': unique_counts})
    
    ax = sns.barplot(plot_df, x = 'name', y = 'frequency', hue='frequency', palette='crest', ax=axs[1])
    axs[1].set_title('Number of carriers from '+airport+' airport on '+ str(day)+'/'+str(month))
    axs[1].tick_params(labelsize=6, labelrotation=90)
    axs[1].set_xlabel('carrier', fontsize=10)
    axs[1].set_ylabel('frequency', fontsize=10)
    axs[1].legend(fontsize=6)
    
    for i in ax.containers:
        ax.bar_label(i,fontsize=6)
        
    plt.show()
    
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
    sns.barplot(airlines_df, x = 'name', y = 'avg_delay', hue='avg_delay', palette='Blues_d')
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
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    plt.rcParams["axes.titlesize"] = 10
    sns.scatterplot(df, x='distance', y='arr_delay', size='arr_delay', sizes=(1, 100), hue='arr_delay', palette='Reds', ax=axs[0])
    axs[0].set_title('The relationship between the distance of a flight and the arrival delay time',fontsize=10)
    axs[0].set_xlabel('Distances')
    axs[0].set_ylabel('Arrival Delay Time')
    
    sns.histplot(data = df['arr_delay'], ax=axs[1])
    axs[1].set_title('Distribution of the arrival delay time', fontsize=10)
    axs[1].set_xlabel('Arrival Delay Time')
    axs[1].set_ylabel('Frequency')
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
    
    export("planes")
    
def compute_wind_direction_from_NYC():
    
    query = f'SELECT faa, lat, lon FROM airports'
    cursor.execute(query)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    JFK = pt1.getJFK()
    NYC_lat = JFK['lat']
    NYC_lon = JFK['lon']
    wind_array = []
    
    for i in range(len(df)):
        this_lat = df['lat'][i]
        this_lon = df['lon'][i]
        
        if(df['faa'][i] != 'JFK'):
            delta_lon = abs(this_lon - NYC_lon)
            x = float(math.cos(NYC_lat) * math.sin(delta_lon))
            y = float(math.cos(this_lat) * math.sin(NYC_lat) - math.sin(this_lat) * math.cos(NYC_lat) * math.cos(delta_lon))
        
            angle = math.degrees(math.atan(y/x))
            wind_array.append(angle)
        else:
            wind_array.append(None)
        
    new_df = df.assign(wind_direction = wind_array)
    
    print(new_df)       
        
    return


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
       
    print(airports_df)
    
    return

def barplot_frequency(table, column):
    
    # table = input('Enter the table name:')
    # column = input('Enter the column name:')
    
    table_df = getTable(table)
    unique_values = table_df[column].unique()
    unique_counts = []
    
    for value in unique_values:
        counter = 0
        counter = table_df[column].value_counts().get(value, 0)
        unique_counts.append(counter)
    
    plot_df = pd.DataFrame({'name': unique_values, 'frequency': unique_counts})
       
    plt.rcParams['figure.figsize'] = [12, 8]
    plt.rcParams["axes.titlesize"] = 20
    plt.rcParams["axes.labelsize"] = 12
    plt.rcParams["xtick.labelsize"] = 6
    plt.title('Number of '+column+ ' in '+table)
    ax = sns.barplot(plot_df, x = 'name', y = 'frequency', hue='frequency', palette='crest')
    plt.xlabel(column)
    plt.xticks(rotation=45)
    plt.ylabel('Frequency')
    
    for i in ax.containers:
        ax.bar_label(i,)
        
    plt.show()
    
    return

def plot_histogram(input_df, column):
    
    plt.figure(figsize=(10, 6))
    plt.title('Distribution of '+column)
    ax = sns.histplot(data = input_df[column])
    plt.xlabel(column, fontsize=10)
    plt.ylabel('frequency',fontsize=10)
    
    for i in ax.containers:
        ax.bar_label(i,fontsize=6)
        
    plt.show()
    
    return

def advanced_time_zones():
    
    pt1.analyzeTimeZone()  
    
    table_df = getTable('airports')
    column_list = ['tz', 'tzone']
    
    fig, axs = plt.subplots(1, 3, figsize=(20, 5))
    plt.rcParams["axes.titlesize"] = 10
    plt.rcParams["axes.labelsize"] = 4
    plt.rcParams["xtick.labelsize"] = 4
    
    for i in range(2):
    
        unique_values = table_df[column_list[i]].unique()
        unique_counts = []
    
        for value in unique_values:
            counter = 0
            counter = table_df[column_list[i]].value_counts().get(value, 0)
            unique_counts.append(counter)
        
        plot_df = pd.DataFrame({'name': unique_values, 'frequency': unique_counts})
    
        ax = sns.barplot(plot_df, x = 'name', y = 'frequency', hue='frequency', palette='crest', ax=axs[i])
        axs[i].set_title('Number of '+column_list[i]+' in airports')
        axs[i].set_xlabel(column_list[i],fontsize=10)
        axs[i].set_ylabel('frequency',fontsize=10)
        axs[i].tick_params(labelsize=6, labelrotation=90)
        axs[i].legend(fontsize=6)
    
        for j in ax.containers:
            ax.bar_label(j,fontsize=6)
    
    table_df = table_df.dropna(subset=['tzone'])
    unique_values = table_df['tzone'].unique()
    unique_counts = []
    
    for value in unique_values:
        counter = 0
        counter = table_df['tzone'].value_counts().get(value, 0)
        unique_counts.append(counter)
    
    table_df = table_df.drop_duplicates(subset=['tzone'])
    table_df = table_df.assign(tzone_counter=unique_counts)
    
    plt.rcParams["legend.markerscale"] = 0.3
    sns.scatterplot(table_df, x='tzone', y='tz', hue='tz', size='tzone_counter', sizes=(100, 1000), palette='RdBu', ax=axs[2])
    axs[2].set_title('Relationship between the distance of \na flight and the arrival delay time')
    axs[2].set_xlabel('tzone',fontsize=10)
    axs[2].set_ylabel('tz',fontsize=10)
    axs[2].tick_params(labelsize=6, labelrotation=90)
    axs[2].legend(fontsize=6)
    
    plt.show()

    return

def analyze_altitude():
        
    table_df = getTable('airports')  
    
    plt.figure(figsize=(10, 6))
    plt.title('Distribution of altitudes of all airports')
    ax = sns.histplot(data = table_df['alt'])
    plt.xlabel('alt', fontsize=10)
    plt.ylabel('frequency',fontsize=10)
    
    for i in ax.containers:
        ax.bar_label(i,fontsize=6)
        
    plt.show()
    
    return

def analyze_seats():
        
    table_df = getTable('planes') 
     
    plt.figure(figsize=(10, 6))
    plt.title('Distribution of seats in planes')
    ax = sns.histplot(data = table_df['seats'], binwidth=50)
    plt.xlabel('seats')
    plt.ylabel('Frequency')
    plt.tick_params(labelsize=6, labelrotation=90)
    
    for i in ax.containers:
        ax.bar_label(i,fontsize=6)
        
    plt.show()
    
    return

def analyze_planes():
    
    table_df = getTable('planes')
    column_list = ['year', 'manufacturer', 'seats', 'engine']
    
    fig, axs = plt.subplots(2, 2, figsize=(18, 12))
    fig.subplots_adjust(wspace=0.5, hspace=0.5)
    plt.rcParams['figure.figsize'] = [6, 4]
    plt.rcParams["axes.titlesize"] = 6
    plt.rcParams["axes.labelsize"] = 4
    plt.rcParams["xtick.labelsize"] = 4
    
    for i in range(2):
        for j in range(2):
            unique_values = table_df[column_list[i*2+j]].unique()
            unique_counts = []
            
            for value in unique_values:
                counter = 0
                counter = table_df[column_list[i*2+j]].value_counts().get(value, 0)
                unique_counts.append(counter)
                
            plot_df = pd.DataFrame({'name': unique_values, 'frequency': unique_counts})
                
            ax = sns.barplot(plot_df, x = 'name', y = 'frequency', hue='frequency', palette='crest', ax=axs[i,j])
            axs[i,j].set_title('Distribution of '+column_list[i*2+j])
            axs[i,j].set_xlabel(column_list[i*2+j], fontsize=6)
            axs[i,j].set_ylabel('frequency', fontsize=6)
            axs[i,j].legend(fontsize=6)
            axs[i,j].tick_params(labelsize=6, labelrotation=90)
            
            for k in ax.containers:
                ax.bar_label(k, fontsize=6)
            
    plt.show()  
        
    return