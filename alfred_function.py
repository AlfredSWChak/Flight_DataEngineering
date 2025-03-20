import sqlite3
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import math

connection = sqlite3.connect('flights_database.db', check_same_thread=False)
cursor = connection.cursor()

def top_five_planes():
    
    query = f'SELECT * FROM planes'
    cursor.execute(query)
    rows = cursor.fetchall()
    planes_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])

    unique_planes_df = planes_df.drop_duplicates(subset=['manufacturer', 'model'])
    
    count_planes_df = planes_df.groupby(by=['manufacturer', 'model']).size().reset_index(name='numPlanes')
    top_five = count_planes_df.sort_values(by=['numPlanes'], ascending=False).head()
    
    result = pd.DataFrame()
    
    for manufacturer, model, numPlanes in zip(top_five['manufacturer'], top_five['model'], top_five['numPlanes']):
        result = pd.concat([result, unique_planes_df[(unique_planes_df['manufacturer'] == manufacturer) & (unique_planes_df['model'] == model)]])
        
    result = result.assign(numPlanes=list(top_five['numPlanes']))
    result = result.drop(columns=['tailnum', 'year'])
    
    return result

def top_five_flights_JFK():
    
    query = f'SELECT * FROM flights WHERE origin = ?'
    cursor.execute(query, ('JFK',))
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])

    unique_planes_df = flights_df.drop_duplicates(subset=['tailnum'])
    
    count_planes_df = flights_df.groupby(by=['tailnum']).size().reset_index(name='numFlights')
    top_five = count_planes_df.sort_values(by=['numFlights'], ascending=False).head()
    
    result = pd.DataFrame()
    
    # for manufacturer, model, numPlanes in zip(top_five['manufacturer'], top_five['model'], top_five['numPlanes']):
    #     result = pd.concat([result, unique_planes_df[(unique_planes_df['manufacturer'] == manufacturer) & (unique_planes_df['model'] == model)]])
        
    # result = result.assign(numPlanes=list(top_five['numPlanes']))
    # result = result.drop(columns=['tailnum', 'year'])
    
    return result

def top_five_flights(airport):
    
    if(airport == 'All airports'):
        query = f'SELECT origin, dest, distance FROM flights'
        cursor.execute(query)
    else:
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

def printTopFiveFlights(origin_list, dest_list):
   
    all_list = origin_list + dest_list
    
    query = f'SELECT * FROM airports WHERE faa IN ({','.join(['?']*len(all_list))})'
    cursor.execute(query, all_list)
    rows = cursor.fetchall()
    airports_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    fig = px.scatter_geo(airports_df, hover_name="name", lat="lat", lon="lon", color="alt", text="faa")  
    
    for origin, dest in zip(origin_list, dest_list):
        origin_lat = airports_df[airports_df['faa']==origin]['lat'].iloc[0]
        origin_lon = airports_df[airports_df['faa']==origin]['lon'].iloc[0]
        dest_lat = airports_df[airports_df['faa']==dest]['lat'].iloc[0]
        dest_lon = airports_df[airports_df['faa']==dest]['lon'].iloc[0]
   
        fig.add_trace(go.Scattergeo(locationmode = 'USA-states',lon = [origin_lon, dest_lon], lat = [origin_lat, dest_lat], mode = "lines", line = dict(width = 1,color = 'red'), opacity = 1))
    
    # fig.update_traces(showlegend=False)
    
    return fig

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
    result = result.drop(columns=['year','tailnum'])
    
    count_planes_df = planes_df.groupby(by=['year']).size().reset_index(name='numModels')
    # count_planes_df = count_planes_df.sort_values(by=['year'], ascending=False)
    # count_planes_df = count_planes_df.drop(columns=['tailnum', 'type', 'manufacturer','model','engines','seats','speed','engine'])
    
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
    
    for tzone in airports_df['tzone']:
        if 'America' in tzone:
            return fig
    
    fig.update_layout(title = 'Trace of the flight',geo_scope="usa")
    
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

def getAirportInfo(airport):
    
    query = f'SELECT * FROM airports WHERE faa = ?'
    cursor.execute(query, (airport,))
    rows = cursor.fetchall()
    airport_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    return airport_df

def getTailnumPlanes(tailnum_list):
    
    query = f'SELECT * FROM planes WHERE tailnum IN ({','.join(['?']*len(tailnum_list))})'
    cursor.execute(query, tailnum_list)
    rows = cursor.fetchall()
    planes_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    return planes_df

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
    
    delta_lon = (origin_lon - dest_lon)
    y = float(math.cos(origin_lat) * math.sin(delta_lon))
    x = float(math.cos(dest_lat) * math.sin(origin_lat) - math.sin(dest_lat) * math.cos(origin_lat) * math.cos(delta_lon))
        
    angle = math.degrees(math.atan2(y ,x))        
    
    return angle