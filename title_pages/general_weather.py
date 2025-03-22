import streamlit as st
import altair as alt
import functions.extra as ex
import functions.part1 as pt1
import functions.part3 as pt3
import functions.airlines as alnes
import functions.flights as flt
import functions.weather as wthr
import calendar
from datetime import datetime

month_list = list(calendar.month_name)[1:]


if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.header('General Information about weather')

c_1 = st.container()
        
with c_1:
    temp = ex.getAirportFullName(['EWR', 'LGA', 'JFK'])
    joined_list = temp[['faa','name']].agg('-'.join, axis=1)
    
    selection = st.sidebar.selectbox('Select an airport', sorted(joined_list))
    airport = selection[:3]
    
    cols = st.columns((4, 4), gap = 'medium')
    
    with cols[0]:
        season = st.radio('Select a season:', ('Spring (March, April, May)', 'Summer (June, July, August)', 'Autumn (September, October, November)', 'Winter (December, Janurary, Feburary)'), horizontal=False)
        month_list = wthr.getMonth(season)
        
    with cols[1]:
        fig, result = wthr.hourlyAverage(airport, month_list)
        st.write(f'***Average*** of {season}')
        st.write('Wind Speed:',round(result['wind_speed'],3),'m/s')
        st.write('Wind Gust:',round(result['wind_gust'],3), 'm/s')
        st.write('Visibility:',round(result['visib'],3),'m')     

c_2 = st.container(border=True)
    
with c_2:
    st.plotly_chart(fig, use_container_width=True)