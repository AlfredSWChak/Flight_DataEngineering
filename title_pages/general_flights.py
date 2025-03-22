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

st.header('General Information on flights')

c_1 = st.container()

with c_1:
    cols = st.columns(2, gap = 'small')
    
    # with cols[0]:
    origin = st.sidebar.selectbox('Select a Departure Airport:',['EWR', 'LGA', 'JFK'])
    dest_list = sorted(pt3.unique_arrive_airports_input(origin))
    dest = st.sidebar.selectbox('Select an Arrival Airport:',dest_list)
    
    with cols[0]:
        st.write('Flight Distance:',ex.get_geodesicDistance(origin, dest),'km')
        st.write('Flight Time:', ex.get_airtime(origin, dest),'minutes')
        st.write('Altitude difference:', ex.get_alt_diff(origin, dest),'m')
        st.write('Time zone difference:', ex.get_tz_diff(origin, dest),'hours')
    
    with cols[1]:
        avg_dep_delay, avg_arr_delay = flt.averageDelay(origin, dest)
        
        st.write('Average ***Departure*** Delay:', avg_dep_delay,'min')
        st.write('Average ***Arrival*** Delay:', avg_arr_delay,'min')
        
        numFlights_month = flt.flightsPerMonth(origin,dest)
        
        st.write('Flights per ***Month***:', numFlights_month)
        
        numFlights_day = flt.flightsPerDay(origin,dest)
        
        st.write('Flights per ***Day***:', numFlights_day)

c_2 = st.container(border=True)

with c_2:
    fig = ex.drawOneFlight(origin, dest)
    fig.update_layout(showlegend=False, dragmode=False)
    fig.update_coloraxes(showscale=False)
    fig.update_layout(hoverlabel_font_color='black', font_color = 'blue')
    fig.update_traces(marker=dict(size=5, color='DarkSlateGrey'), textposition='top center')
    
    st.plotly_chart(fig, use_container_width=True)
    
    result = ex.available_carrier(origin, dest)
    
    carrier = st.radio('Select an airline:', set(result['carrier']), horizontal=True)

    numPlanes, new_result = ex.available_plane_model(origin, dest, carrier)
    st.write('There are',numPlanes, 'planes served by', carrier+'.')
    
    result, bar_result = ex.check_plane_model(list(new_result['tailnum']))
    
    result_copy = result.copy()
    result_copy.columns = ['Manufacturer', 'Model', 'Number of engines', 'Seats', 'Speed (m/s)', 'Engine']
    st.write('There are',len(result),'unique models:')
    st.dataframe(result_copy.set_index(result_copy.columns[0]), use_container_width=True)
    
c_3 = st.container(border=True)

with c_3: 
    fig = flt.get_flights_number(origin, dest)
    st.plotly_chart(fig, use_container_width=True)