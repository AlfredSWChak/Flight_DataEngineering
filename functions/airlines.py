import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

connection = sqlite3.connect('flights_database.db', check_same_thread=False)
cursor = connection.cursor()

def showAllAirports():
    
    query = f'SELECT * FROM airports'
    cursor.execute(query)
    rows = cursor.fetchall()
    airports_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    fig = px.scatter_geo(airports_df, hover_name='name', 
                         lat='lat', 
                         lon = 'lon', 
                         color='alt',
                         color_continuous_scale='rainbow',
                         size_max=1)
    fig.update_layout(title = 'All the airports with different altitudes')
    fig.update_coloraxes(colorbar_title_text='Altitude of airports')
    
    return fig

def getAirlines_list():
    
    query = f'SELECT * FROM airlines'
    cursor.execute(query)
    rows = cursor.fetchall()
    airlines_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    return airlines_df

def getAllTailnum(airline):

    query = f'SELECT carrier, tailnum FROM flights WHERE carrier = ?'
    cursor.execute(query, (airline,))
    rows = cursor.fetchall()
    tailnum_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    
    unique_tailnum = tailnum_df.drop_duplicates(subset=['tailnum'])
    tailnum_list = list(unique_tailnum['tailnum'])
    
    query = f'SELECT * FROM planes WHERE tailnum IN ({','.join(['?']*len(tailnum_list))})'
    cursor.execute(query, tailnum_list)
    rows = cursor.fetchall()
    models_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    numOfPlanes = len(models_df)
    
    unique_models_df = models_df.drop_duplicates(subset=['manufacturer','model'])
    
    numOfUniqueModels = len(unique_models_df)
    
    count_unique_models_df = models_df.groupby(by=['manufacturer','model','seats']).size().reset_index(name='numModels')
    count_unique_models_df = count_unique_models_df.sort_values(by=['manufacturer'], ascending=True)
    
    count_years_df = models_df.groupby(by=['manufacturer','model','year']).size().reset_index(name='numModels')
    count_years_df['year'] = count_years_df['year'].astype(int)
    count_years_df = count_years_df.sort_values(by=['manufacturer'], ascending=True)
    
    return count_unique_models_df, numOfPlanes, numOfUniqueModels, count_years_df, models_df

def getModelsList(models_df, manufacturer):
    
    models_list = models_df[models_df['manufacturer'] == manufacturer]['model']
    
    return models_list

def getModelStatistics(scope, unique_models_df, models_df):
    
    if scope == 'Manufacturer':
        manus_df = models_df.groupby(by=['manufacturer']).size().reset_index(name='numModels')
        fig = px.pie(manus_df, values='numModels', names='manufacturer', title='Proportions of different plane manufacturer of the whole fleet', color_discrete_sequence=px.colors.sequential.Aggrnyl)
    
    elif scope == 'Model':
        fig = px.pie(unique_models_df, values='numModels', names='model', title='Proportions of different plane models of the whole fleet', color_discrete_sequence=px.colors.sequential.Aggrnyl)
    
    elif scope == 'Year':
        years_df = models_df.groupby(by=['year']).size().reset_index(name='numModels')
        fig = px.pie(years_df, values='numModels', names='year', title='Proportions of different plane year of the whole fleet', color_discrete_sequence=px.colors.sequential.Aggrnyl)
        
    
    else:
        return fig
    
    return fig

def getOldestModels(count_years_df):
    
    manufacturer = count_years_df[count_years_df['year'] == count_years_df['year'].min()]['manufacturer'].iloc[0]
    model = count_years_df[count_years_df['year'] == count_years_df['year'].min()]['model'].iloc[0]
    numModel = count_years_df[count_years_df['year'] == count_years_df['year'].min()]['numModels'].iloc[0]
    year = count_years_df[count_years_df['year'] == count_years_df['year'].min()]['year'].iloc[0]  
    
    return manufacturer, model, numModel, year

def getYoungestModels(count_years_df):
    
    manufacturer = count_years_df[count_years_df['year'] == count_years_df['year'].max()]['manufacturer'].iloc[0]
    model = count_years_df[count_years_df['year'] == count_years_df['year'].max()]['model'].iloc[0]
    numModel = count_years_df[count_years_df['year'] == count_years_df['year'].max()]['numModels'].iloc[0]
    year = count_years_df[count_years_df['year'] == count_years_df['year'].max()]['year'].iloc[0]  
    
    return manufacturer, model, numModel, year