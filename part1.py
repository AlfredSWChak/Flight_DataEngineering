import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import math

file = pd.read_csv("airports_original.csv")
        
# fig = px.scatter_geo(file, hover_name="name", lat="lat", lon = "lon", color="alt")
fig = px.scatter_geo()

def drawLine(inputFAA, fig):

    new_df = pd.DataFrame(columns = ["faa", "name", "lat", "lon", "alt", "tz", "dst", "tzone"])
    
    NYC_lat = 0.0
    NYC_lon = 0.0
    input_lat = 0.0
    input_lon = 0.0
    
    for i in range(len(file)):
        
        if (inputFAA == file["faa"][i]):
           input_lat = file.iloc[i] ["lat"]
           input_lon = file.iloc[i] ["lon"]
           new_df.loc[i] = file.iloc[i]
        elif (file["faa"][i] == "JFK"):
           NYC_lat = file.iloc[i] ["lat"]
           NYC_lon = file.iloc[i] ["lon"]
           new_df.loc[i] = file.iloc[i]
    
    print(new_df)
    
    fig = px.scatter_geo(new_df, hover_name="name", lat="lat", lon="lon", color="alt", text="faa")
    # fig.update_layout(title = 'Map of US.',geo_scope="usa")
    fig.add_trace(go.Scattergeo(locationmode = 'USA-states',lon = [input_lon, NYC_lon], lat = [input_lat, NYC_lat], mode = "lines", line = dict(width = 1,color = 'red'), opacity = 1))
    fig.show()
    return fig

def drawMultipleLines(faaList, month, day, origin_faa):
    
    new_df = pd.DataFrame(columns = ["faa", "name", "lat", "lon", "alt", "tz", "dst", "tzone"])
    
    for i in range(len(faaList)):
        for j in range(len(file)):
            input_lat = 0.0
            input_lon = 0.0
                
            if (faaList[i] == file["faa"][j]):
                input_lat = file.iloc[j] ["lat"]
                input_lon = file.iloc[j] ["lon"]
                new_df.loc[j] = file.iloc[j]
    
    origin_row = getAirportRow(origin_faa).iloc[0]
    # NYC_row = getJFK().iloc[0]
    origin_lon = origin_row["lon"]
    origin_lat = origin_row["lat"]
    new_df.loc[origin_row.index[0]] = origin_row
    
    fig = px.scatter_geo(new_df, hover_name="name", lat="lat", lon="lon", color="alt", text="faa")  
    
    for i in range(len(new_df) - 1):
        input_lon = new_df.iloc[i]["lon"]
        input_lat = new_df.iloc[i]["lat"]
        fig.add_trace(go.Scattergeo(locationmode = 'USA-states',lon = [input_lon, origin_lon], lat = [input_lat, origin_lat], mode = "lines", line = dict(width = 1,color = 'red'), opacity = 1))
    
    fig.update_layout(title_text = 'Flights to New York from specific locations', showlegend = False)
    fig.update_layout(title = 'Map of Flight from ' + origin_faa + ' on ' + str(day) + '/' + str(month) ,geo_scope="usa")
    fig.show()
    return

def getJFK():
    JFK_df = pd.DataFrame(columns = ["faa", "name", "lat", "lon", "alt", "tz", "dst", "tzone"])
    
    for i in range(len(file)):
        if (file["faa"][i] == "JFK"):
            JFK_df.loc[i] = file.iloc[i]  
    
    return JFK_df

def getAirportRow(airport):
    airport_row = pd.DataFrame(columns = ["faa", "name", "lat", "lon", "alt", "tz", "dst", "tzone"])
    
    for i in range(len(file)):
        if (file["faa"][i] == airport):
            airport_row.loc[i] = file.iloc[i]  
    
    return airport_row

def calculateDistances():
    
    NYC_row = getJFK().iloc[0]
    NYC_lon = NYC_row["lon"]
    NYC_lat = NYC_row["lat"]
    distance_np = np.array([])
    
    for i in range(len(file)):
        thisAirport = file.iloc[i] 
        distance = math.sqrt((thisAirport["lon"] -  NYC_lon)**2 + (thisAirport["lat"] - NYC_lat)**2)
        distance_np = np.append(distance_np, distance)
    
    plt.figure(figsize=(10, 6))
    plt.title('Distribution of the distances to John F. Kennedy Airport')
    sns.histplot(data = distance_np, binrange=[min(distance_np), max(distance_np)])
    plt.xlabel('Distances')
    plt.ylabel('Frequency')
    plt.show()
    return distance_np

# randomlists = ["ALX", "BKC", "BKG", "HOT", "LFI", "MLL", "PBF", "TUP"]
# drawMultipleLines(randomlists)

earthRadius = 6378

def geodesicDistance():
    
    NYC_row = getJFK().iloc[0]
    NYC_lon = NYC_row["lon"]
    NYC_lat = NYC_row["lat"]
    distance_np = np.array([])
    
    for i in range(len(file)):
        thisAirport = file.iloc[i] 
        deltaLon = math.radians(thisAirport["lon"] - NYC_lon)
        deltaLat = math.radians(thisAirport["lat"] - NYC_lat)
        midPointLat =  math.radians((thisAirport["lat"] + NYC_lat ) / 2)
        
        distance = earthRadius * math.sqrt((2 * math.sin(deltaLat/2) * math.cos(deltaLon/2))**2 + (2 * math.cos(midPointLat) * math.sin(deltaLon/2))**2)
        distance_np = np.append(distance_np, distance)
    
    plt.figure(figsize=(10, 6))
    plt.title('Distribution of the distances to John F. Kennedy Airport')
    sns.histplot(data = distance_np, binrange=[min(distance_np), max(distance_np)])
    plt.xlabel('Distances')
    plt.ylabel('Frequency')
    plt.show()
    
    return distance_np

def analyzeTimeZone():

    tz_file = file.dropna(subset=['tz'])

    fig = px.scatter_geo(tz_file, hover_name="name", lat="lat", lon="lon", color="tz")
    fig.show()
    
    return

# def getCity():

#     cityList = []
    
#     for i in range(len(file)):
#         thisAirport = file.iloc[i]
        
#         if (pd.isnull(thisAirport['tzone'])):
#             city = thisAirport['tzone']
#         else:
#             city = thisAirport['tzone'].split('/')[1]
#             city = city.replace('_',' ')   
             
#         cityList.append(city)
    
#     newFile = file.assign(citys = cityList)
#     newFile = newFile.dropna(subset=['citys'])
    
#     statesFile = pd.read_csv("states.csv")
#     abbrevList = []
    
#     for i in range(len(newFile)):
#         thisAirport = newFile.iloc[i]
        
#         for j in range(len(statesFile)):
#             if (thisAirport['citys'] == statesFile.iloc[j]['State']):
#                 abbrev = statesFile.iloc[j]['Abbreviation']
#                 break
        
#         abbrevList.append(abbrev)
    
#     newFile = newFile.assign(abbrevs = abbrevList)
    
#     print(newFile)
    
#     return

# getCity()