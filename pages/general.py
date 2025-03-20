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

options_set = ('General Information of **Airports**',
               'General Information of **Airlines**',
               'General Information of **Flights**',
               'Flight statistics on a specific day',
               'Flight statistics for delay',
               'Delay analysis - Possible causes: Weather 🌦️')
month_list = list(calendar.month_name)[1:]

add_selectbox = st.sidebar.radio('Options', 
                                 options=options_set, 
                                 label_visibility='hidden'
)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

if add_selectbox == 'Flight statistics on a specific day':
    st.header('Flight statistics on a specific day')

    c_1 = st.container()
        
    with c_1:
        date = st.date_input('Select a date', value=None, min_value='2023-01-01', max_value='2023-12-31')
        airport = st.selectbox('Select an airport',['EWR', 'LGA', 'JFK'])
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
        
elif add_selectbox == 'Delay analysis - Possible causes: Weather 🌦️':
    st.header('Delay analysis - Possible causes: Weather 🌦️')
    
    origin = st.selectbox('Select Departure Airport:',['EWR', 'LGA', 'JFK'])
    dest_list = sorted(pt3.unique_arrive_airports_input(origin))
    dest = st.selectbox('Select Arrival Airport:',dest_list)
    
    input_start_month = st.selectbox('Select the month of start:',month_list)
    input_end_month = st.selectbox('Select the end of month',month_list[month_list.index(input_start_month):])
    
    button_clicked = st.button('Submit')
    
    c_1 = st.container(border=True)
    
    with c_1:
        if button_clicked:
            
            start_month = datetime.strptime(input_start_month, '%B').month
            end_month = datetime.strptime(input_end_month, '%B').month
            
            wind_fig, visib_fig, dest_direction, num_delay, num_non_delay = flt.delayDotProduct(start_month, end_month, origin, dest)
            
            st.write('For destination',dest,'during month',input_start_month,'to',input_end_month,', the amount of flights is',num_delay+num_non_delay,'.')
            st.write('There are',num_delay,'delay flights, and',num_non_delay,'non-delay flights.')
            st.write(f'The angle between **{origin}** and **{dest}** is', round(dest_direction,2), 'degrees.')
            
            cols = st.columns(2, gap = 'small')
        
            with cols[0]:
                st.plotly_chart(wind_fig, use_container_width=True)
            with cols[1]:
                st.plotly_chart(visib_fig, use_container_width=True)
  
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
        
    st.subheader('Top five common flights of selected airport(s)')
    
    c_2 = st.container()
        
    with c_2:
        airport = st.selectbox('Select a departure airport',['EWR', 'LGA', 'JFK', 'All airports'])
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
    st.header('General Information on airlines')
    
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
        st.write(f'The oldest plane model in use is **{manufacturer}-{model}**. There are',numModel, 'models made in',str(year),'.')
            
        manufacturer, model, numModel, year = alnes.getYoungestModels(count_years_df)
        st.write(f'The youngest plane model in use is **{manufacturer}-{model}**. There are',numModel,'models made in',str(year),'.')
        
        # st.table(count_years_df.set_index(count_years_df.columns[0]))
        
        cols = st.columns(2, gap = 'small')
        
        with cols[0]:
            unique_models_df_copy = unique_models_df.copy()
            unique_models_df_copy.columns = ['Manufacturer', 'Model', 'Seats', 'Number of planes']
            st.table(unique_models_df_copy.set_index(unique_models_df_copy.columns[0]))
        with cols[1]:
            st.bar_chart(data=unique_models_df, x='model', y='numModels', horizontal=True, use_container_width=True)
              
        # manufacturer = st.selectbox('Select a model:', sorted(set(manufacturers_list)))
        
        # models_list = alnes.getModelsList(models_df, manufacturer)
        # model = st.selectbox('Select a model:', sorted(set(models_list)))
        
        fig = alnes.getModelStatistics(unique_models_df)
        st.plotly_chart(fig, use_container_width=True)
        
elif add_selectbox == 'General Information of **Flights**':
    st.header('General Information on flights')
    
    c_1 = st.container()
    
    with c_1:
        cols = st.columns(3, gap = 'small')
        
        with cols[0]:
            origin = st.selectbox('Select a Departure Airport:',['EWR', 'LGA', 'JFK'])
            dest_list = sorted(pt3.unique_arrive_airports_input(origin))
            dest = st.selectbox('Select an Arrival Airport:',dest_list)
        
        with cols[1]:
            st.write('Flight Distance:',af.get_geodesicDistance(origin, dest),'km')
            st.write('Flight Time:', af.get_airtime(origin, dest),'minutes')
            st.write('Altitude difference:', af.get_alt_diff(origin, dest),'m')
            st.write('Time zone difference:', af.get_tz_diff(origin, dest),'hours')
        
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
        
        carrier = st.radio('Select an airline:', set(result['carrier']))
    
        numPlanes, new_result = af.available_plane_model(origin, dest, carrier)
        st.write('There are',numPlanes, 'planes served by', carrier+'.')
        
        result, bar_result = af.check_plane_model(list(new_result['tailnum']))
        
        st.write('There are',len(result),'unique models:')
        st.table(result.set_index(result.columns[0]))

elif add_selectbox == 'Flight statistics for delay':
    st.header('Flight Statistics for Delay')

    origin = st.selectbox('Select Departture Airport:', ['EWR', 'LGA', 'JKF'])
    destination_options = flt.get_all_destinations(origin)
    dest = st.selectbox('Select Destination Airport:', destination_options)

    flights_df = flt.get_flight_data()
    filtered_df = flights_df[(flights_df['origin'] == origin) & (flights_df['dest'] == dest)]

    if not filtered_df.empty:
        st.subheader(f"Flight Delay Statistics from {origin} to {dest}")
        st.write(f"Total Flights: {len(filtered_df)}")
        st.write(f"Average Weekly Flights: {len(filtered_df) / 52:.2f}")
        st.write(f"Average Flight Time: {filtered_df['air_time'].mean():.2f} minutes")
        st.write(f"Average Delay: {filtered_df['dep_delay'].mean():.2f} minutes")

        st.subheader("Flights per Month")
        flights_per_month = flights_df['month'].value_counts().sort_index()
        st.bar_chart(flights_per_month)

        st.subheader("Total Delay per Month")
        delay_per_month = flights_df.groupby('month')['dep_delay'].sum().sort_index()
        st.bar_chart(delay_per_month)

    else:
        st.write("No flight data found for the selected route.")

bkhm = st.sidebar.button("Back to home page", icon='🔙') 

if bkhm:
    st.switch_page("home.py") 
