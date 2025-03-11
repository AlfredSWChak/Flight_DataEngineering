import streamlit as st
import altair as alt
import alfred_function as af
import part3 as pt3
import calendar
from datetime import datetime

st.sidebar.title('Functions')

options_set = ('Flight statistics on specific day', 
            #    'Top five plane models', 
            #    'Top five flights',
               'Among of delay flights',
               'Check available carrier for flight')
month_list = list(calendar.month_name)[1:]

add_selectbox = st.sidebar.radio('Options', 
                                 options=options_set, 
                                 label_visibility='hidden'
)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

if add_selectbox == 'Flight statistics on specific day':
    st.header('Flight statistics on specific day')

    c_1 = st.container()
        
    with c_1:
        date = st.date_input('Select a date', value=None)
        airport = st.selectbox('Select a airport',['EWR', 'LGA', 'JFK'])
        button_clicked = st.button('Submit')
        
    c_2 = st.container(border=True)  
        
    with c_2:
        if button_clicked:
            
            month = date.month
            day = date.day
            
            numFlights, numUniqueDest, destMost, numMost =  pt3.printStatisticsOnDateAtAirport(month, day, airport)
            
            st.text('On '+str(day)+'/'+str(month)+' at '+airport+', there are '+str(numFlights)+' flights.')
            st.text('On '+str(day)+'/'+str(month)+' at '+airport+', there are '+str(numUniqueDest)+' unique destinations.')
            st.text('On '+str(day)+'/'+str(month)+' at '+airport+', '+destMost+' is visited most often with '+str(numMost)+' flights.')
            
            fig = pt3.printFlightsOnDateAtAirport(month, day, airport)
            
            st.plotly_chart(fig, use_container_width=True)
            
# elif add_selectbox == 'Top five plane models':
#     st.header('The top 5 plane models are:')
    
#     c_1 = st.container(border=True)
    
#     with c_1:
#         result = af.top_five_planes()
#         st.table(result.set_index(result.columns[0]))
        
# elif add_selectbox == 'Top five flights':
#     st.header('Top 5 flights')
    
#     c_1 = st.container()
    
#     with c_1:
#         airport = st.selectbox('Select a airport',['EWR', 'LGA', 'JFK', 'All airports'])
#         button_clicked = st.button('Submit')
        
#     c_2 = st.container(border=True)  
        
#     with c_2:
#         if button_clicked:
#             result = af.top_five_flights(airport)
#             st.table(result.set_index(result.columns[0]))
        
elif add_selectbox == 'Among of delay flights':
    st.header('Among of delay flights')
    
    input_start_month = st.selectbox('Select the month of start:',month_list)
    input_end_month = st.selectbox('Select the end of month',month_list[month_list.index(input_start_month):])
    
    dest_list = sorted(pt3.unique_arrive_airports())
    dest = st.selectbox('Select a destination airport',dest_list)
    button_clicked = st.button('Submit')
    
    c_1 = st.container(border=True)
    
    with c_1:
        if button_clicked:
            
            start_month = datetime.strptime(input_start_month, '%B').month
            end_month = datetime.strptime(input_end_month, '%B').month
            amount = pt3.amongOfDelayFlights(start_month, end_month, dest)
            
            st.write('For destination',dest,'during month',input_start_month,'to',input_end_month,', the amount of delay flights is',amount,'.')
            
elif add_selectbox == 'Check available carrier for flight':
    st.header('Available carrier')
    
    c_1 = st.container()
    
    with c_1:
        cols = st.columns((4, 4), gap = 'medium')
        
        with cols[0]:
            origin = st.selectbox('Select Departure Airport:',['EWR', 'LGA', 'JFK'])
            dest_list = sorted(pt3.unique_arrive_airports_input(origin))
            dest = st.selectbox('Select Arrival Airport:',dest_list)
        
        with cols[1]:
            st.subheader('General Information of the flight')
            st.write('Distance of flight:',af.get_geodesicDistance(origin, dest),'km')
            st.write('Time of flight:', af.get_airtime(origin, dest),'minutes')
            st.write('Altitude difference between:', af.get_altdiff(origin, dest),'m')
            
    
    c_2 = st.container(border=True)
    
    with c_2:
        fig = af.drawOneFlight(origin, dest)
        st.plotly_chart(fig, use_container_width=True)
        
        result = af.available_carrier(origin, dest)
        st.table(result.set_index(result.columns[0]))
        
        carrier = st.radio('Select an airline:', set(result['carrier']))
    
        numPlanes, new_result = af.available_plane_model(origin, dest, carrier)
        st.write('There are',numPlanes, 'planes served by', carrier+'.')
        
        result, bar_result = af.check_plane_model(list(new_result['tailnum']))
        
        st.write('There are',len(result),'unique models:')
        st.table(result.set_index(result.columns[0]))
        
        bar_chart = alt.Chart(bar_result, title='Number of planes in each year').mark_bar().encode(x='year', y='numModels')
        st.altair_chart(bar_chart,use_container_width=True)