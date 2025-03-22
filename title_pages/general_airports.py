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

st.header('General Information of airports')

c_1 = st.container(border=True)
    
with c_1:
    fig = pt1.showAllAirports()
    area = st.radio('Select a scope:', ('World', 'USA'
                                        # , 'Europe', 'Asia', 'Africa', 'North America', 'South America'
                                        ), horizontal=True)
    fig.update_layout(geo_scope=area.lower())
    fig.update_layout(dragmode=False)
    st.plotly_chart(fig, use_container_width=True)
    
st.subheader('Airport General Information')

c_4 = st.container()

with c_4:
    airport_df = pt3.getTable('airports')
    temp = ex.getAirportFullName(airport_df['faa'])
    joined_list = temp[['faa','name']].agg('-'.join, axis=1)
    
    selection = st.sidebar.selectbox('Select an Airport:', joined_list)
    airport = selection[:3]
    
    cols = st.columns(2, gap = 'small')
    
    with cols[0]:
        airport_row = ex.getAirportInfo(airport)
        st.write(f'Full name: :blue[{airport_row['name'][0]}]')
        st.write(f'Daylight savings: :blue[{ex.getDSTMeaning(airport_row['dst'][0])}]')
        st.write('Time Zone: GMT',airport_row['tz'][0])
    
    with cols[1]:
        airport_row = ex.getAirportInfo(airport)
        st.write('Latitude: ',airport_row['lat'][0],'°')
        st.write('Longitude: ',airport_row['lon'][0],'°')
        st.write('Altitude: ',airport_row['alt'][0],'m')
        
c_5 = st.container(border=True)

with c_5: 
    unique_origin = pt3.unique_depart_airports_input(airport)
    
    if (len(unique_origin) == 0):
        st.write(f'There are no flights data about :red[{selection}].')
    elif (len(unique_origin) == 1):
        st.write(f':blue[{selection}] can be flied from: :blue[{unique_origin[0]}].')
    elif (len(unique_origin) == 2):
        st.write(f':blue[{selection}] can be flied from: :blue[{unique_origin[0]}] and :blue[{unique_origin[1]}].')
    elif (len(unique_origin) == 3):
        st.write(f':blue[{selection}] can be flied from: :blue[{unique_origin[0]}], :blue[{unique_origin[1]}] and :blue[{unique_origin[2]}].')
    
    fig = ex.printOneAirport(airport)
    fig.update_layout(dragmode=False)
    st.plotly_chart(fig, use_container_width=True)