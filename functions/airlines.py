import sqlite3
import math
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

connection = sqlite3.connect('flights_database.db', check_same_thread=False)
cursor = connection.cursor()

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
    
    return count_unique_models_df, numOfPlanes, numOfUniqueModels, count_years_df

def getModelsList(models_df, manufacturer):
    
    models_list = models_df[models_df['manufacturer'] == manufacturer]['model']
    
    return models_list

def getModelStatistics(models_df):
    
    # new_models_df = models_df[models_df['model'] == model]
    
    # count_year_df = models_df.groupby(by=['year']).size().reset_index(name='numModels')
    # count_year_df = count_year_df.sort_values(by=['year'], ascending=False)
    
    fig = px.pie(models_df, values='numModels', names='model', title='Proportions of different plane models of the whole fleet', color_discrete_sequence=px.colors.sequential.Aggrnyl)
    
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