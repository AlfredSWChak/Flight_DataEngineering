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
               'General Information of **Weather**',
               'Flight statistics on a specific day')

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
        
        temp = ex.getAirportFullName(['EWR', 'LGA', 'JFK'])
        joined_list = temp[['faa','name']].agg('-'.join, axis=1)
        
        selection = st.selectbox('Select an airport', sorted(joined_list))
        airport = selection[:3]
    
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
            fig.update_layout(showlegend=False, dragmode=False)
            fig.update_coloraxes(showscale=False)
            fig.update_layout(hoverlabel_font_color='black', font_color = 'blue')
            fig.update_traces(marker=dict(size=5, color='DarkSlateGrey'), textposition='top center')
            
            st.plotly_chart(fig, use_container_width=True)
  
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
            temp = ex.getAirportFullName(airport_df['faa'])
            joined_list = temp[['faa','name']].agg('-'.join, axis=1)
            
            selection = st.selectbox('Select an Airport:', joined_list)
            airport = selection[:3]
            
        with cols[1]:
            airport_row = ex.getAirportInfo(airport)
            st.write('Full name: ',airport_row['name'][0])
            st.write('Altitude: ',airport_row['alt'][0],'m')
            st.write('Time Zone: GMT',airport_row['tz'][0])
            
    c_5 = st.container(border=True)
    
    with c_5: 
        fig = ex.printOneAirport(airport)
        fig.update_layout(dragmode=False)
        st.plotly_chart(fig, use_container_width=True)
        
    st.subheader('Top five common flights of selected airport(s)')
    
    c_2 = st.container()
        
    with c_2:
        temp = ex.getAirportFullName(['EWR', 'LGA', 'JFK'])
        joined_list = temp[['faa','name']].agg('-'.join, axis=1)
        
        selection = st.selectbox('Select a departure airport', sorted(joined_list))
        airport = selection[:3]
        
        button_clicked = st.button('Submit')   
       
    c_3 = st.container(border=True)
        
    with c_3:   
        if button_clicked:
            result = ex.top_five_flights(airport)
            fig = ex.printTopFiveFlights(list(result['origin']), list(result['dest']))
            
            fig.update_layout(geo_scope='usa')
            fig.update_layout(title = f'Top five flights of {airport}')
            fig.update_layout(showlegend=False, dragmode=False)
            fig.update_layout(hoverlabel_font_color='black', font_color = 'blue')
            fig.update_traces(marker=dict(size=5, color='DarkSlateGrey'), textposition='top center')
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
            st.write('Flight Distance:',ex.get_geodesicDistance(origin, dest),'km')
            st.write('Flight Time:', ex.get_airtime(origin, dest),'minutes')
            st.write('Altitude difference:', ex.get_alt_diff(origin, dest),'m')
            st.write('Time zone difference:', ex.get_tz_diff(origin, dest),'hours')
        
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
        result_copy.columns = ['Type', 'Manufacturer', 'Model', 'Number of engines', 'Seats', 'Speed', 'Engine']
        
        st.write('There are',len(result),'unique models:')
        st.table(result_copy.set_index(result_copy.columns[0]))

elif add_selectbox == 'General Information of **Weather**':
    st.header('General Information about weather')

    c_1 = st.container()
            
    with c_1:
        temp = ex.getAirportFullName(['EWR', 'LGA', 'JFK'])
        joined_list = temp[['faa','name']].agg('-'.join, axis=1)
        
        selection = st.selectbox('Select an airport', sorted(joined_list))
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