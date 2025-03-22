import sqlite3
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import math
import numpy as np
from numpy import pi, sin, cos

connection = sqlite3.connect('flights_database.db', check_same_thread=False)
cursor = connection.cursor()

def getTailnumPlanes(tailnum_list):
    
    query = f'SELECT * FROM planes WHERE tailnum IN ({','.join(['?']*len(tailnum_list))})'
    cursor.execute(query, tailnum_list)
    rows = cursor.fetchall()
    planes_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    return planes_df

def top_five_planes(airport):
    
    query = f'SELECT * FROM flights WHERE origin = ?'
    cursor.execute(query, (airport,))
    rows = cursor.fetchall()
    flights_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    count_tailnum_df = flights_df.groupby(by=['tailnum']).size().reset_index(name='numTailnum')
    sorted_count_tailnum_df = count_tailnum_df.sort_values(by=['tailnum'], ascending=True)
    
    unique_tailnum = sorted_count_tailnum_df.drop_duplicates(subset=['tailnum'])
    tailnum_list = list(unique_tailnum['tailnum'])
    
    planes_df = getTailnumPlanes(tailnum_list)
    planes_df = planes_df.sort_values(by=['tailnum'], ascending=True)
    planes_df = planes_df.assign(numTailnum=count_tailnum_df['numTailnum'])
    
    unique_planes_df = planes_df.drop_duplicates(subset=['manufacturer', 'model'])
    numPlanes_count_list = []
    
    for manufacturer, model in zip(unique_planes_df['manufacturer'], unique_planes_df['model']):
        this_numPlanes = planes_df.loc[(planes_df['manufacturer'] == manufacturer) & (planes_df['model'] == model), 'numTailnum'].sum()
        numPlanes_count_list.append(this_numPlanes)
    
    result = unique_planes_df.assign(numPlanes=numPlanes_count_list)
    result = result.sort_values(by=['numPlanes'], ascending=False).head()
    result = result.drop(columns=['tailnum','year','numTailnum'])
    
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
    
    fig = px.scatter_geo(airports_df, hover_name="name", lat="lat", lon="lon", text="faa")  
    
    for origin, dest in zip(origin_list, dest_list):
        origin_lat = airports_df[airports_df['faa']==origin]['lat'].iloc[0]
        origin_lon = airports_df[airports_df['faa']==origin]['lon'].iloc[0]
        dest_lat = airports_df[airports_df['faa']==dest]['lat'].iloc[0]
        dest_lon = airports_df[airports_df['faa']==dest]['lon'].iloc[0]
   
        fig.add_trace(go.Scattergeo(locationmode = 'USA-states',lon = [origin_lon, dest_lon], lat = [origin_lat, dest_lat], mode = "lines", line = dict(width = 1,color = 'red'), opacity = 1))
    
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
    result = result.drop(columns=['year','tailnum', 'type'])
    
    count_planes_df = planes_df.groupby(by=['year']).size().reset_index(name='numModels')
    # count_planes_df = count_planes_df.sort_values(by=['year'], ascending=False)
    # count_planes_df = count_planes_df.drop(columns=['tailnum', 'type', 'manufacturer','model','engines','seats','speed','engine'])
    
    return result, count_planes_df

def point_sphere(lon, lat):
    #associate the cartesian coords (x, y, z) to a point on the  globe of given lon and lat
    #lon longitude
    #lat latitude
    lon = lon*pi/180
    lat = lat*pi/180
    x = cos(lon) * cos(lat) 
    y = sin(lon) * cos(lat) 
    z = sin(lat) 
    return np.array([x, y, z])

def slerp(A=[100, 45], B=[-50, -25], dir=-1, n=100):
    #Spherical "linear" interpolation
    """
    A=[lonA, latA] lon, lat given in degrees; lon in  (-180, 180], lat in (-90, 90]
    B=[lonB, latB]
    returns n points on the great circle of the globe that passes through the  points A, B
    #represented by lon and lat
    #if dir=1 it returns the shortest path; for dir=-1 the complement of the shortest path
    """
    As = point_sphere(A[0], A[1])
    Bs = point_sphere(B[0], B[1])
    alpha = np.arccos(np.dot(As,Bs)) if dir==1 else  2*pi-np.arccos(np.dot(As,Bs))
    
    if abs(alpha) < 1e-6 or abs(alpha-2*pi)<1e-6:
        return A
    else:
        t = np.linspace(0, 1, n)
        P = sin((1 - t)*alpha) 
        Q = sin(t*alpha)
        #pts records the cartesian coordinates of the points on the chosen path
        pts =  np.array([a*As + b*Bs for (a, b) in zip(P,Q)])/sin(alpha)
        #convert cartesian coords to lons and lats to be passed to go.Scattermapbox
        lons = 180*np.arctan2(pts[:, 1], pts[:, 0])/pi
        lats = 180*np.arctan(pts[:, 2]/np.sqrt(pts[:, 0]**2+pts[:,1]**2))/pi
        
        return lons, lats

def drawOneFlight(origin, dest):
    
    keys = [origin, dest]
    
    query = f'SELECT * FROM airports WHERE faa IN ({','.join(['?']*len(keys))})'
    cursor.execute(query, keys)
    rows = cursor.fetchall()
    airports_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    # origin_lat = airports_df[airports_df['faa'] == origin]['lat'].iloc[0]
    # origin_lon = airports_df[airports_df['faa'] == origin]['lon'].iloc[0]
    # dest_lat = airports_df[airports_df['faa'] == dest]['lat'].iloc[0]
    # dest_lon = airports_df[airports_df['faa'] == dest]['lon'].iloc[0]
    
    fig = px.scatter_geo(airports_df, hover_name="name", lat="lat", lon="lon", color="alt", text="faa")  
    
    # lons, lats = slerp(A=[origin_lon, origin_lat], B=[dest_lon, dest_lat], dir=1)
    # fig.add_trace(go.Scattergeo(locationmode = 'USA-states', lon=lons, lat=lats, mode="lines", line_color="red"))
    
    fig.update_layout(title = 'Trace of the flight',geo_scope="usa")
    fig.add_trace(go.Scattergeo(locationmode = 'USA-states',lon = airports_df['lon'], lat = airports_df['lat'], mode = "lines", line = dict(width = 1,color = 'red'), opacity = 1))
    
    for tzone in airports_df[airports_df['faa'] == dest]['tzone']:
        if 'America' in tzone:
            return fig
    
    fig.update_layout(title = 'Trace of the flight',geo_scope="world")
    
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

def getAirportFullName(airports_list):
    
    query = f'SELECT * FROM airports WHERE faa IN ({','.join(['?']*len(airports_list))})'
    cursor.execute(query, airports_list)
    rows = cursor.fetchall()
    airports_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    return airports_df

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
                      xaxis=dict(title=dict(text=scope), type='category'),yaxis=dict(title=dict(text='Number of flights')))
    fig.update_layout(plot_bgcolor='white')      
 
    return fig

def printN_NYC_airports():
    
    NYC_list = ['EWR', 'JFK', 'LGA']
    
    NYC_df = getAirportFullName(NYC_list)
    
    fig = go.Figure()
    fig.add_trace(go.Scattermap(lon = [NYC_df['lon'].iloc[0]], lat = [NYC_df['lat'].iloc[0]], mode = "markers", marker = dict(color = 'blue', size=10), opacity = 1, name='EWR'))
    fig.add_trace(go.Scattermap(lon = [NYC_df['lon'].iloc[1]], lat = [NYC_df['lat'].iloc[1]], mode = "markers", marker = dict(color = 'red', size=10), opacity = 1, name='JFK'))
    fig.add_trace(go.Scattermap(lon = [NYC_df['lon'].iloc[2]], lat = [NYC_df['lat'].iloc[2]], mode = "markers", marker = dict(color = 'green', size=10), opacity = 1, name='LGA'))
    # fig.update_layout(title = 'Airports in NYC')
    fig.update_layout(showlegend=False)
    fig.update_layout(
        map=dict(center=dict(lat=40.730610, lon=-73.935242), # this will center on the point
        zoom=8))
    
    return fig