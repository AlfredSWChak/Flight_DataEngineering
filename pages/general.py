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

st.sidebar.title('Functions')

options_set = ('General Information of **Airports**',
               'General Information of **Airlines**',
               'General Information of **Flights**',
               'General Information of **Weather**')

month_list = list(calendar.month_name)[1:]

add_selectbox = st.sidebar.radio('Options', 
                                 options=options_set, 
                                 label_visibility='hidden'
)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

if add_selectbox == 'General Information of **Airports**':
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
            
elif add_selectbox == 'General Information of **Airlines**':
    st.header('General Information on airlines')
    
    c_1 = st.container()
    
    with c_1:
        temp = alnes.getAirlines_list()
        joined_df = temp[['carrier','name']].agg('-'.join, axis=1)

        airline = st.sidebar.selectbox('Select an airline:', sorted(set(joined_df)))
        airline_abbrv = airline[:2]
        airline_fullName = airline[3:]
        
    c_2 = st.container(border=True)
    
    with c_2:
        unique_models_df, numOfPlanes, numOfUniqueModels, count_years_df, models_df = alnes.getAllTailnum(airline_abbrv)
        st.write(airline_fullName,'has total', numOfPlanes,'planes. ',numOfUniqueModels,'different models are provided.')
        
        manufacturer, model, numModel, year = alnes.getOldestModels(count_years_df)
        st.write(f'The oldest plane model in use is **{manufacturer}-{model}**. There are',numModel, 'models made in',str(year),'.')
            
        manufacturer, model, numModel, year = alnes.getYoungestModels(count_years_df)
        st.write(f'The youngest plane model in use is **{manufacturer}-{model}**. There are',numModel,'models made in',str(year),'.')
        
        # st.table(count_years_df.set_index(count_years_df.columns[0]))
        
        # cols = st.columns(2, gap = 'small')
        
        # with cols[0]:
        
    c_3 = st.container()
    
    with c_3:
        unique_models_df_copy = unique_models_df.copy()
        unique_models_df_copy.columns = ['Manufacturer', 'Model', 'Seats', 'Number of planes']
        st.dataframe(unique_models_df_copy.set_index(unique_models_df_copy.columns[0]), use_container_width=True)
        
        # with cols[1]:
    c_4 = st.container()
    
    # with c_4:
    #     agg_list = unique_models_df[['manufacturer', 'model']].agg('-'.join, axis=1)
    #     unique_models_df['model'] = list(agg_list)
    #     plot_df = unique_models_df.rename(columns={'model': 'Model', 'numModels': 'Number of models'})
    #     st.bar_chart(data= plot_df, x='Model', y='Number of models', horizontal=True, use_container_width=True)
        
    c_5 = st.container(border=True)
    
    with c_5:
        scope = st.radio('Select a scope:', ('Model', 'Manufacturer', 'Year'), horizontal=True)
        
        fig = alnes.getModelStatistics(scope, unique_models_df, models_df)
        st.plotly_chart(fig, use_container_width=True)
        
elif add_selectbox == 'General Information of **Flights**':
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
        

elif add_selectbox == 'General Information of **Weather**':
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

bkhm = st.sidebar.button("Back to home page", icon='🔙') 

if bkhm:
    st.switch_page("home.py") 