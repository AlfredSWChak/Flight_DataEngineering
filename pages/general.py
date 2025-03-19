import streamlit as st
import altair as alt
import alfred_function as af
import part1 as pt1
import part3 as pt3
import functions.airlines as alnes
import functions.flights as flt
import calendar
from datetime import datetime

st.sidebar.title('Functions')

options_set = ('General Information of Airports',
               'General Information of Airlines',
               'General Information of Flights',
            #    'General Information of Weather',
               'Flight statistics on specific day',
               'Amount of delay for flights')
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
        button_clicked = st.button('Select')
        
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
        
elif add_selectbox == 'General Information of **Airports**':
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
        cols = st.columns((4, 4), gap = 'medium')
        
        with cols[0]:
            airport_df = pt3.getTable('airports')
            airport = st.selectbox('Select an Airport:', airport_df['faa'])
            
        with cols[1]:
            airport_row = af.getAirportInfo(airport)
            st.write('Full name: ',airport_row['name'][0])
            st.write('Altitude: ',airport_row['alt'][0],'m')
            st.write('Time Zone: GMT',airport_row['tz'][0])
            
    c_5 = st.container(border=True)
    
    with c_5: 
        fig = af.printOneAirport(airport)
        fig.update_layout(dragmode=False)
        st.plotly_chart(fig, use_container_width=True)
        
    st.subheader('Top five flights of selected airport(s)')
    
    c_2 = st.container()
        
    with c_2:
        airport = st.selectbox('Select a deaprture airport',['EWR', 'LGA', 'JFK', 'All airports'])
        button_clicked = st.button('Submit')   
       
    c_3 = st.container(border=True)
        
    with c_3:   
        if button_clicked:
            result = af.top_five_flights(airport)
            fig = af.printTopFiveFlights(list(result['origin']), list(result['dest']))
            
            fig.update_layout(geo_scope='usa')
            fig.update_layout(title = f'Top five flights of {airport}')
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(fig, use_container_width=True)
            result = result.drop(columns=['origin'])
            st.table(result.set_index(result.columns[0]))
            
elif add_selectbox == 'General Information of **Airlines**':
    st.header('General Information of airlines')
    
    c_1 = st.container()
    
    with c_1:
        temp = alnes.getAirlines_list()
        joined_df = temp[['carrier','name']].agg('-'.join, axis=1)

        airline = st.selectbox('Select an airline:', sorted(set(joined_df)))
        airline_abbrv = airline[:2]
        airline_fullName = airline[3:]
        
    c_2 = st.container()
    
    with c_2:
        unique_models_df, numOfPlanes, numOfUniqueModels, count_years_df = alnes.getAllTailnum(airline_abbrv)
        st.write(airline_fullName,'has total', numOfPlanes,'planes. ',numOfUniqueModels,'different models are provided.')
        
        manufacturer, model, numModel, year = alnes.getOldestModels(count_years_df)
        st.write(f'The oldest plane model is **{manufacturer}-{model}**. There are',numModel,' models made in',str(year),'.')
            
        manufacturer, model, numModel, year = alnes.getYoungestModels(count_years_df)
        st.write(f'The youngest plane model is **{manufacturer}-{model}**. There are',numModel,'models made in',str(year),'.')
        
        # st.table(count_years_df.set_index(count_years_df.columns[0]))
        
        cols = st.columns(2, gap = 'small')
        
        with cols[0]:
            st.table(unique_models_df.set_index(unique_models_df.columns[0]))
        with cols[1]:
            st.bar_chart(data=unique_models_df, x='model', y='numModels', horizontal=True, use_container_width=True)
              
        # manufacturer = st.selectbox('Select a model:', sorted(set(manufacturers_list)))
        
        # models_list = alnes.getModelsList(models_df, manufacturer)
        # model = st.selectbox('Select a model:', sorted(set(models_list)))
        
        fig = alnes.getModelStatistics(unique_models_df)
        st.plotly_chart(fig, use_container_width=True)
        
elif add_selectbox == 'General Information of **Flights**':
    st.header('General Information of flights')
    
    c_1 = st.container()
    
    with c_1:
        cols = st.columns(3, gap = 'small')
        
        with cols[0]:
            origin = st.selectbox('Select Departure Airport:',['EWR', 'LGA', 'JFK'])
            dest_list = sorted(pt3.unique_arrive_airports_input(origin))
            dest = st.selectbox('Select Arrival Airport:',dest_list)
        
        with cols[1]:
            st.write('Distance of flight:',af.get_geodesicDistance(origin, dest),'km')
            st.write('Time of flight:', af.get_airtime(origin, dest),'minutes')
            st.write('Altitude difference between:', af.get_alt_diff(origin, dest),'m')
            st.write('Time zone difference between:', af.get_tz_diff(origin, dest),'hours')
        
        with cols[2]:
            avg_dep_delay, avg_arr_delay = flt.averageDelay(origin, dest)
            
            st.write('Average ***Departure*** Delay:', avg_dep_delay,'min')
            st.write('Average ***Arrival*** Delay:', avg_arr_delay,'min')
            
            numFlights_month = flt.flightsPerMonth(origin,dest)
            
            st.write('Flights per ***Month***:', numFlights_month)
            
            numFlights_day = flt.flightsPerDay(origin,dest)
            
            st.write('Flights per ***Day***:', numFlights_day)
    
    c_2 = st.container(border=True)
    
    with c_2:
        fig = af.drawOneFlight(origin, dest)
        st.plotly_chart(fig, use_container_width=True)
        
        result = af.available_carrier(origin, dest)
        # st.table(result.set_index(result.columns[0]))
        
        carrier = st.radio('Select an airline:', set(result['carrier']))
    
        numPlanes, new_result = af.available_plane_model(origin, dest, carrier)
        st.write('There are',numPlanes, 'planes served by', carrier+'.')
        
        result, bar_result = af.check_plane_model(list(new_result['tailnum']))
        
        st.write('There are',len(result),'unique models:')
        st.table(result.set_index(result.columns[0]))

bkhm = st.sidebar.button("Back to home page", icon='🔙') 

if bkhm:
    st.switch_page("home.py") 
