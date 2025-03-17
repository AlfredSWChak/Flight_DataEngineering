import sqlite3
import math
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

connection = sqlite3.connect('flights_database.db')
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
    model_df = pd.DataFrame(rows, columns = [x[0] for x in cursor.description])
    numOfPlanes = len(model_df)
    
    unique_models_df = model_df.drop_duplicates(subset=['manufacturer','model'])
    numOfUniqueModels = len(unique_models_df)
    
    manufacturers_list = unique_models_df['manufacturer']
    
    return model_df, numOfPlanes, numOfUniqueModels, manufacturers_list

def getModelsList(models_df, manufacturer):
    
    models_list = models_df[models_df['manufacturer'] == manufacturer]['model']
    
    return models_list

def getModelStatistics(models_df, model):
    
    new_models_df = models_df[models_df['model'] == model]
    
    count_year_df = new_models_df.groupby(by=['year']).size().reset_index(name='numModels')
    count_year_df = count_year_df.sort_values(by=['year'], ascending=False)
    
    return count_year_df