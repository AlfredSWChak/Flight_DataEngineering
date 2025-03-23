import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import sqlite3

import functions.part1 as pt1
import functions.part3 as pt3
import functions.part4 as pt4

import altair as alt
import functions.extra as ex
import functions.airlines as alnes
import functions.flights as flt
import calendar
from datetime import datetime
import matplotlib.pyplot as plt

month_list = list(calendar.month_name)[1:]

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.header('Delay analysis - Possible causes: Weather 🌦️')

temp_origin = ex.getAirportFullName(['EWR', 'LGA', 'JFK'])
joined_list = temp_origin[['faa','name']].agg('-'.join, axis=1)
    
origin_selection = st.sidebar.selectbox('Select Departure Airport:', sorted(joined_list))
origin = origin_selection[:3]

dest_list = sorted(pt3.unique_arrive_airports_input(origin))
temp_dest = ex.getAirportFullName(dest_list)
joined_dest_list = temp_dest[['faa','name']].agg('-'.join, axis=1)
    
dest_selection = st.sidebar.selectbox('Select Arrival Airport:', sorted(joined_dest_list))
dest = dest_selection[:3]

input_start_month = st.selectbox('Select the month of departure:',month_list)
input_end_month = st.selectbox('Select the month of arrival:',month_list[month_list.index(input_start_month):])

button_clicked = st.button('Select')

c_1 = st.container(border=True)

with c_1:
    if button_clicked:
        
        start_month = datetime.strptime(input_start_month, '%B').month
        end_month = datetime.strptime(input_end_month, '%B').month
        
        wind_fig, visib_fig, dest_direction, num_delay, num_non_delay, direction_fig = flt.delayDotProduct(start_month, end_month, origin, dest)
        
        st.write('For destination',dest,'during month',input_start_month,'to',input_end_month,', the amount of flights is',num_delay+num_non_delay,'.')
        st.write('There are',num_delay,'delay flights, and',num_non_delay,'non-delay flights.')
        st.write(f'The azimuth between **{origin}** and **{dest}** is', round(dest_direction,2), 'degrees.')
        
        # cols = st.columns(2, gap = 'small')
    
        # with cols[0]:
        st.plotly_chart(wind_fig, use_container_width=True)
        # with cols[1]:
        st.plotly_chart(direction_fig, use_container_width=True) 
            
        # st.plotly_chart(visib_fig, use_container_width=True)
          
