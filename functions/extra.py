import sqlite3
import pandas as pd
import numpy as np
from numpy import pi, sin, cos
import math
import plotly.express as px
import plotly.graph_objects as go
import functions.manipulating as mp

connection = sqlite3.connect('flights_database.db', check_same_thread=False)
cursor = connection.cursor()

def top_five_planes(airport):
    
    query = f'SELECT * FROM flights WHERE origin = ?'
    cursor.execute(query, (airport,))
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    count_tailnum_df = flights_df.groupby(by=['tailnum']).size().reset_index(name='numTailnum')
    
    tailnum_list = list(count_tailnum_df['tailnum'])
   
    planes_df = mp.getTailnumPlanes(tailnum_list)
    
    numTailnum_list = []
    
    for item in planes_df['tailnum']:
        
        if item in count_tailnum_df['tailnum'].values:
           numTailnum = count_tailnum_df[count_tailnum_df['tailnum'] == item]['numTailnum'].iloc[0]
        else:
            numTailnum = 0
        
        numTailnum_list.append(numTailnum)
        
    planes_df['numTailnum'] = numTailnum_list
        
    unique_planes_df = planes_df.drop_duplicates(subset=['manufacturer', 'model'])
    numPlanes_count_list = []
    
    for manufacturer, model in zip(unique_planes_df['manufacturer'], unique_planes_df['model']):
        this_numPlanes = planes_df.loc[(planes_df['manufacturer'] == manufacturer) & (planes_df['model'] == model), 'numTailnum'].sum()
        numPlanes_count_list.append(this_numPlanes)
    
    result = unique_planes_df.assign(numPlanes=numPlanes_count_list)
    result = result.sort_values(by=['numPlanes'], ascending=False).head()
    result = result.drop(columns=['type','tailnum','year','numTailnum'])
    
    return result

def top_five_airlines(airport):
    
    query = f'SELECT * FROM flights WHERE origin = ?'
    cursor.execute(query, (airport,))
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    count_df = flights_df.groupby(by=['carrier']).size().reset_index(name='numFlights')
    
    query = f'SELECT * FROM airlines'
    cursor.execute(query)
    rows = cursor.fetchall()
    airlines_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    numFlights_list = []
    
    for item in airlines_df['carrier']:
        
        if item in count_df['carrier'].values:
           numFlights = count_df[count_df['carrier'] == item]['numFlights'].iloc[0]
        else:
            numFlights = 0
        
        numFlights_list.append(numFlights)
        
    airlines_df['numFlights'] = numFlights_list
        
    result = airlines_df.sort_values(by=['numFlights'], ascending=False)
    
    fig = px.pie(count_df, values='numFlights', names='carrier', title=f'Proportions of different airlines departed from {airport}', color_discrete_sequence=px.colors.sequential.Aggrnyl)
    fig.update_layout(legend=dict(title=dict(text='Airlines', font_color='grey')))
    
    return fig, result

def top_five_flights(airport):
    
    query = f'SELECT origin, dest, distance FROM flights WHERE origin = ?'
    cursor.execute(query, (airport,))
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    unique_flights_df = flights_df.drop_duplicates(subset=['origin', 'dest'])
    
    count_flights_df = flights_df.groupby(by=['origin', 'dest']).size().reset_index(name='numFlights')
    top_five = count_flights_df.sort_values(by=['numFlights'], ascending=False).head()
    
    result = pd.DataFrame()
    
    for origin, dest, numFlights in zip(top_five['origin'], top_five['dest'], top_five['numFlights']):
        result = pd.concat([result, unique_flights_df[(unique_flights_df['origin'] == origin) & (unique_flights_df['dest'] == dest)]])
    
    result = result.assign(numFlights=list(top_five['numFlights']))
    result = result.astype({'distance':'int'})
    
    return result

def printFlightsOnDateAtAirport(month, day, airport):
    
    query = f'SELECT month, day, carrier, origin, dest, distance FROM flights WHERE month = ? AND day = ? AND origin = ?'
    cursor.execute(query, [month, day, airport])
    rows = cursor.fetchall()
    new_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
        
    destinationList = new_df['dest']
    
    result = drawMultipleLines(destinationList, month, day, airport)
    
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

def printOneAirport(airport):
    
    query = f'SELECT * FROM airports WHERE faa = ?'
    cursor.execute(query, (airport,))
    rows = cursor.fetchall()
    airport_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
   
    fig = px.scatter_geo(airport_df, hover_name='name', 
                         lat='lat', 
                         lon = 'lon',
                         size_max=1)
    fig.update_layout(title = 'The location of the airport')
    fig.update_traces(marker_color='red', selector=dict(type='scattergeo'))
    fig.update_traces(marker_symbol="star",selector=dict(type='scattergeo'))
    fig.update_traces(marker_size=10, selector=dict(type='scattergeo'))
    
    return fig

def printTopFiveFlights(origin_list, dest_list):
   
    all_list = origin_list + dest_list
    
    query = f'SELECT * FROM airports WHERE faa IN ({','.join(['?']*len(all_list))})'
    cursor.execute(query, all_list)
    rows = cursor.fetchall()
    airports_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    fig = px.scatter_geo(airports_df, hover_name="name", lat="lat", lon="lon", text="faa")  
    
    for origin, dest in zip(origin_list, dest_list):
        origin_lat = airports_df[airports_df['faa']==origin]['lat'].iloc[0]
        origin_lon = airports_df[airports_df['faa']==origin]['lon'].iloc[0]
        dest_lat = airports_df[airports_df['faa']==dest]['lat'].iloc[0]
        dest_lon = airports_df[airports_df['faa']==dest]['lon'].iloc[0]
   
        fig.add_trace(go.Scattergeo(locationmode = 'USA-states',lon = [origin_lon, dest_lon], lat = [origin_lat, dest_lat], mode = "lines", line = dict(width = 1,color = 'red'), opacity = 1))
    
    return fig

def print_NYC_airports():
    
    NYC_list = ['EWR', 'JFK', 'LGA']
    
    NYC_df = mp.getAirportsListInfo(NYC_list)
    
    fig = go.Figure()
    fig.add_trace(go.Scattermap(lon = [NYC_df['lon'].iloc[0]], lat = [NYC_df['lat'].iloc[0]], mode = "markers", marker = dict(color = 'blue', size=10), opacity = 1, name='EWR'))
    fig.add_trace(go.Scattermap(lon = [NYC_df['lon'].iloc[1]], lat = [NYC_df['lat'].iloc[1]], mode = "markers", marker = dict(color = 'red', size=10), opacity = 1, name='JFK'))
    fig.add_trace(go.Scattermap(lon = [NYC_df['lon'].iloc[2]], lat = [NYC_df['lat'].iloc[2]], mode = "markers", marker = dict(color = 'green', size=10), opacity = 1, name='LGA'))
    # fig.update_layout(title = 'Airports in NYC')
    fig.update_layout(showlegend=False)
    fig.update_layout(map=dict(center=dict(lat=40.712776, lon=-74.005974),zoom=8))
    
    return fig

def printUniqueDestinations():
    
    fig = go.Figure()
    
    dest_list = mp.unique_arrive_airports_input('EWR')
    EWR_numUnique_dest = unique_dest_input(dest_list)
    numUnique_dest_df = mp.getAirportsListInfo(EWR_numUnique_dest)
    fig.add_traces(go.Scattermap(hovertext=numUnique_dest_df['faa'], lon = numUnique_dest_df['lon'], lat = numUnique_dest_df['lat'], mode = "markers", marker = dict(color = 'blue', size=5), opacity = 1, name='EWR'))
    
    dest_list = mp.unique_arrive_airports_input('JFK')
    JFK_numUnique_dest = unique_dest_input(dest_list)
    numUnique_dest_df = mp.getAirportsListInfo(JFK_numUnique_dest)
    fig.add_traces(go.Scattermap(hovertext=numUnique_dest_df['faa'], lon = numUnique_dest_df['lon'], lat = numUnique_dest_df['lat'], mode = "markers", marker = dict(color = 'red', size=5), opacity = 1, name='JFK'))
    
    dest_list = mp.unique_arrive_airports_input('LGA')
    LGA_numUnique_dest = unique_dest_input(dest_list)
    numUnique_dest_df = mp.getAirportsListInfo(LGA_numUnique_dest)
    fig.add_traces(go.Scattermap(hovertext=numUnique_dest_df['faa'], lon = numUnique_dest_df['lon'], lat = numUnique_dest_df['lat'], mode = "markers", marker = dict(color = 'green', size=5), opacity = 1, name='LGA'))
    
    fig.update_layout(title = 'Unique destinations departed from each airport',map=dict(center=dict(lat=54.525963,lon=-105.255119),style='light'),)
    fig.update_layout(legend=dict(title=dict(text='Depart from', font_color='grey')))
    
    return EWR_numUnique_dest, JFK_numUnique_dest, LGA_numUnique_dest, fig

def available_carrier(origin, dest):
    
    query = f'SELECT origin, dest, carrier FROM flights WHERE origin = ? AND dest = ?'
    cursor.execute(query, (origin, dest,))
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    unique_flights_df = flights_df.drop_duplicates(subset=['carrier'])   
    result = unique_flights_df
    
    return result

def available_plane_model(origin, dest, carrier):
    
    query = f'SELECT origin, dest, carrier, tailnum FROM flights WHERE origin = ? AND dest = ? AND carrier = ?'
    cursor.execute(query, (origin, dest, carrier,))
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])

    new_df = flights_df[flights_df['carrier'] == carrier].drop_duplicates(subset=['tailnum']) 
    numPlanes = len(new_df)
    
    return numPlanes, new_df

def check_plane_model(tailnum_list):
    
    query = f'SELECT * FROM planes WHERE tailnum IN ({','.join(['?']*len(tailnum_list))})'
    cursor.execute(query, tailnum_list)
    rows = cursor.fetchall()
    planes_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    result = planes_df.drop_duplicates(subset=['manufacturer', 'model'])
    result = result.drop(columns=['year','tailnum', 'type'])
    
    count_planes_df = planes_df.groupby(by=['year']).size().reset_index(name='numModels')
    
    return result, count_planes_df

def drawOneFlight(origin, dest):
    
    keys = [origin, dest]
    
    query = f'SELECT * FROM airports WHERE faa IN ({','.join(['?']*len(keys))})'
    cursor.execute(query, keys)
    rows = cursor.fetchall()
    airports_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    fig = px.scatter_geo(airports_df, hover_name="name", lat="lat", lon="lon", color="alt", text="faa")  
    
    fig.update_layout(title = 'Trace of the flight',geo_scope="usa")
    fig.add_trace(go.Scattergeo(locationmode = 'USA-states',lon = airports_df['lon'], lat = airports_df['lat'], mode = "lines", line = dict(width = 1,color = 'red'), opacity = 1))
    
    for tzone in airports_df[airports_df['faa'] == dest]['tzone']:
        if 'America' in tzone:
            return fig
    
    fig.update_layout(title = 'Trace of the flight',geo_scope="world")
    
    return fig

def drawMultipleLines(faaList, month, day, origin_faa):
    
    airports_df = mp.getTable('airports')
    
    new_df = pd.DataFrame(columns = ["faa", "name", "lat", "lon", "alt", "tz", "dst", "tzone"])
    
    for i in range(len(faaList)):
        for j in range(len(airports_df)):
            input_lat = 0.0
            input_lon = 0.0
                
            if (faaList[i] == airports_df["faa"][j]):
                input_lat = airports_df.iloc[j] ["lat"]
                input_lon = airports_df.iloc[j] ["lon"]
                new_df.loc[j] = airports_df.iloc[j]
    
    origin_row = mp.getAirportRow(origin_faa).iloc[0]
    origin_lon = origin_row["lon"]
    origin_lat = origin_row["lat"]
    new_df.loc[origin_row.index[0]] = origin_row
    
    fig = px.scatter_geo(new_df, hover_name="name", lat="lat", lon="lon", color="alt", text="faa")  
    
    for i in range(len(new_df) - 1):
        input_lon = new_df.iloc[i]["lon"]
        input_lat = new_df.iloc[i]["lat"]
        fig.add_trace(go.Scattergeo(locationmode = 'USA-states',lon = [input_lon, origin_lon], lat = [input_lat, origin_lat], mode = "lines", line = dict(width = 1,color = 'red'), opacity = 1))
    
    fig.update_layout(title_text = 'Flights to New York from specific locations', showlegend = False)
    fig.update_layout(title = 'Flights departed from ' + origin_faa + ' on ' + str(day) + '/' + str(month) ,geo_scope="usa")

    return fig

def get_geodesicDistance(origin, dest):
    
    earthRadius = 6378
    
    keys = [origin, dest]
    
    query = f'SELECT * FROM airports WHERE faa IN ({','.join(['?']*len(keys))})'
    cursor.execute(query, keys)
    rows = cursor.fetchall()
    airports_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    deltaLon = math.radians(airports_df['lon'][0] - airports_df['lon'][1])
    deltaLat = math.radians(airports_df['lat'][0] - airports_df['lat'][1])
    midPointLat =  math.radians((airports_df['lat'].sum()) / 2)
        
    distance = earthRadius * math.sqrt((2 * math.sin(deltaLat/2) * math.cos(deltaLon/2))**2 + (2 * math.cos(midPointLat) * math.sin(deltaLon/2))**2)
    distance = round(distance, 0)

    return distance

def get_airtime(origin, dest):
    
    query = f'SELECT origin, dest, air_time FROM flights WHERE origin = ? AND dest = ?'
    cursor.execute(query, (origin, dest,))
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    result = flights_df['air_time'].mean()
    result = round(result,0)
    
    return result

def get_alt_diff(origin, dest):
    
    keys = [origin, dest]
    
    query = f'SELECT * FROM airports WHERE faa IN ({','.join(['?']*len(keys))})'
    cursor.execute(query, keys)
    rows = cursor.fetchall()
    airports_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    result = abs(airports_df['alt'][0] - airports_df['alt'][1])
    result = round(result,0)
    
    return result

def get_tz_diff(origin, dest):
    
    keys = [origin, dest]
    
    query = f'SELECT * FROM airports WHERE faa IN ({','.join(['?']*len(keys))})'
    cursor.execute(query, keys)
    rows = cursor.fetchall()
    airports_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    result = airports_df['tz'][0] - airports_df['tz'][1]
    
    return result

def getAngleBetween(origin, dest):
    
    faa_list = [origin, dest]
    
    query = f'SELECT faa, lat, lon FROM airports WHERE faa IN ({','.join(['?']*len(faa_list))})'
    cursor.execute(query, faa_list)
    rows = cursor.fetchall()
    airports_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    origin_lat = airports_df[airports_df['faa'] == origin]['lat'].iloc[0]
    origin_lon = airports_df[airports_df['faa'] == origin]['lon'].iloc[0]
    dest_lat = airports_df[airports_df['faa'] == dest]['lat'].iloc[0]
    dest_lon = airports_df[airports_df['faa'] == dest]['lon'].iloc[0]
    
    delta_lon = (dest_lon - origin_lon)
    y = float(math.cos(math.radians(dest_lat)) * math.sin(math.radians(delta_lon)))
    x = float(math.cos(math.radians(origin_lat)) * math.sin(math.radians(dest_lat)) - math.sin(math.radians(origin_lat)) * math.cos(math.radians(dest_lat)) * math.cos(math.radians(delta_lon)))
        
    angle = math.degrees(math.atan2(y ,x))        
    
    return angle

def getDSTMeaning(input):
    
    if input == 'A':
        result = 'Standard US'
    elif input == 'U':
        result = 'Unknown'
    elif input == 'N':
        result = 'No'
    elif input == None:
        result = 'Unknown'
    
    return result

def number_of_flights(origin, scope, graph):
    
    scope = scope.lower()
    
    query = f'SELECT * FROM flights WHERE origin = ?'
    cursor.execute(query, (origin,))
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    count_flights_df = flights_df.groupby(by=[scope]).size().reset_index(name='numFlights')
    new_df = pd.DataFrame(columns=[scope, 'numFlights'])
    
    if scope == 'month':
        new_df[scope] = list(range(1,13))
    elif scope == 'day':
        new_df[scope] = list(range(1,32))
    elif scope == 'hour':
        new_df[scope] = list(range(0,25))
        
    num_list = []
    
    for item, numFlights in zip(new_df[scope], new_df['numFlights']):
        
        if item in count_flights_df[scope].values:
            numFlights = count_flights_df[count_flights_df[scope] == item]['numFlights'].iloc[0]
            
        else:
            numFlights = 0
            
        num_list.append(numFlights)
        
    new_df['numFlights'] = num_list
    
    avg_numFlights= np.mean(num_list)
    
    if graph:
        return new_df
    else:
        return avg_numFlights

def number_of_flights_graph(scope):
    
    title_scope = scope
    scope = scope.lower()
    
    EWR_df = number_of_flights('EWR', scope, True)
    JFK_df = number_of_flights('JFK', scope, True)
    LGA_df = number_of_flights('LGA', scope, True)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=EWR_df[scope], y=EWR_df['numFlights'], name='EWR',
                         line=dict(color='blue', width=2), mode='lines+markers'))
    fig.add_trace(go.Scatter(x=JFK_df[scope], y=JFK_df['numFlights'], name='JFK',
                         line=dict(color='red', width=2), mode='lines+markers'))
    fig.add_trace(go.Scatter(x=LGA_df[scope], y=LGA_df['numFlights'], name='LGA',
                         line=dict(color='green', width=2), mode='lines+markers'))
    fig.update_layout(title=f'Number of flights departed from NYC',
                      xaxis=dict(title=dict(text=title_scope), type='category'),yaxis=dict(title=dict(text='Number of flights')))
    fig.update_layout(plot_bgcolor='white')      
 
    return fig

def number_of_airlines(airport):
    
    query = f'SELECT carrier FROM flights WHERE origin = ?'
    cursor.execute(query, (airport,))
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    carrier_list = flights_df.drop_duplicates()['carrier'].tolist()
    
    numAirlines = len(carrier_list)
    
    return numAirlines

def number_of_models(airport):
    
    query = f'SELECT tailnum FROM flights WHERE origin = ?'
    cursor.execute(query, (airport,))
    rows = cursor.fetchall()
    tailnum_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    tailnum_list = tailnum_df.drop_duplicates()['tailnum'].tolist()
    
    planes_df = mp.getTailnumPlanes(tailnum_list)
    
    model_list = planes_df.drop_duplicates(subset=['model'])['model'].tolist()
    
    numModels = len(model_list)
    
    return numModels

def unique_dest_input(dest_list):
    numUnique_dest = 0
    unique_dest_list = []
    
    for dest in dest_list:
        if len(mp.unique_depart_airports_input(dest)) == 1:
            unique_dest_list.append(dest)
    
    return unique_dest_list
