import streamlit as st
import functions.extra as ex
import functions.flights as flt

st.header('General Information on flights')

c_1 = st.container()

with c_1:
    temp_origin = ex.getAirportFullName(['EWR', 'LGA', 'JFK'])
    joined_origin_list = temp_origin[['faa','name']].agg('-'.join, axis=1)

    origin_selection = st.sidebar.selectbox('Select Departure Airport:', sorted(joined_origin_list))
    origin = origin_selection[:3]

    dest_list = sorted(ex.unique_arrive_airports_input(origin))
    temp_dest = ex.getAirportFullName(dest_list)
    joined_dest_list = temp_dest[['faa','name']].agg('-'.join, axis=1)

    dest_selection = st.sidebar.selectbox('Select Arrival Airport:', sorted(joined_dest_list))
    dest = dest_selection[:3]
    
    cols = st.columns(2, gap = 'small')
    
    with cols[0]:
        flight_distance = ex.get_geodesicDistance(origin, dest)
        flight_time = ex.get_airtime(origin, dest)
        alt_difference = ex.get_alt_diff(origin, dest)
        tz_difference = ex.get_tz_diff(origin, dest)
        
        st.write('Flight Distance:',flight_distance,'km')
        st.write('Flight Time:',flight_time,'minutes')
        st.write('Altitude difference:',alt_difference,'m')
        st.write('Time zone difference:',tz_difference,'hours')
    
    with cols[1]:
        avg_dep_delay, avg_arr_delay = flt.averageDelay(origin, dest)
        numFlights_month = flt.flightsPerMonth(origin,dest)
        numFlights_day = flt.flightsPerDay(origin,dest)
                
        st.write('Average ***Departure*** Delay:', avg_dep_delay,'min')
        st.write('Average ***Arrival*** Delay:', avg_arr_delay,'min')
        st.write('Flights per ***Month***:', numFlights_month) 
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
    result, bar_result = ex.check_plane_model(list(new_result['tailnum']))
    
    st.write('There are',numPlanes, 'planes served by', carrier+'.')
    st.write('There are',len(result),'unique models:')
    
    result_copy = result.copy()
    result_copy.columns = ['Manufacturer', 'Model', 'Number of engines', 'Seats', 'Speed (m/s)', 'Engine']
    st.dataframe(result_copy.set_index(result_copy.columns[0]), use_container_width=True)
    
c_3 = st.container(border=True)

with c_3: 
    fig = flt.get_flights_number(origin, dest)
    st.plotly_chart(fig, use_container_width=True)