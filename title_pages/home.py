import streamlit as st
import functions.extra as ex

st.title('General statistics of the flights departing from NYC')

cols = st.columns((3,3), gap='small')

with cols[0]:
    st.header('THREE airports in NYC')
    st.write(':blue[EWR]: Newark Liberty International Airport')
    st.write(':red[JFK]: John F Kennedy International Airport')
    st.write(':green[LGA]: La Guardia Airport')

with cols[1]:
    fig = ex.print_NYC_airports()
    st.plotly_chart(fig, use_container_width=True)

# cols = st.columns(3, gap='small', border=True)

# with cols[0]:
#     avg_numFlights = ex.number_of_flights('EWR', scope, False)
#     st.write('<p style="color:Blue; font-size: 25px;">EWR</p>', unsafe_allow_html=True)
#     st.write('<p style="font-size: 12px;">Newark Liberty International Airport</p>', unsafe_allow_html=True)
#     st.write(round(avg_numFlights))
# with cols[1]:
#     avg_numFlights = ex.number_of_flights('JFK', scope, False)
#     st.write('<p style="color:Red; font-size: 25px;">JFK</p>', unsafe_allow_html=True)
#     st.write('<p style="font-size: 12px;">John F Kennedy International Airport</p>', unsafe_allow_html=True)
#     st.write(round(avg_numFlights))
# with cols[2]:
#     avg_numFlights = ex.number_of_flights('LGA', scope, False)
#     st.write('<p style="color:Green; font-size: 25px;">LGA</p>', unsafe_allow_html=True)
#     st.write('<p style="font-size: 12px;">La Guardia Airport</p>', unsafe_allow_html=True)
#     st.write(round(avg_numFlights))

c_1 = st.container(border=False)
    
with c_1:
    cols = st.columns(3, gap='small', border=True)

    with cols[0]:
        dest_list = ex.unique_arrive_airports_input('EWR')
        st.write('<p style="color:Blue; font-size: 25px;">EWR</p>', unsafe_allow_html=True)
        # st.write('<p style="font-size: 12px;">Newark Liberty International Airport</p>', unsafe_allow_html=True)
        st.write('Destinations:', len(dest_list))
        numUnique_dest = ex.unique_dest_input(dest_list)
        st.write('Unique destinations:', len(numUnique_dest))
        numAirlines = ex.number_of_airlines('EWR')
        st.write('Airlines:', numAirlines)
        numModels = ex.number_of_models('EWR')
        st.write('Plane models:', numModels)
    with cols[1]:
        dest_list = ex.unique_arrive_airports_input('JFK')
        st.write('<p style="color:Red; font-size: 25px;">JFK</p>', unsafe_allow_html=True)
        # st.write('<p style="font-size: 12px;">John F Kennedy International Airport</p>', unsafe_allow_html=True)
        st.write('Destinations:', len(dest_list))
        numUnique_dest = ex.unique_dest_input(dest_list)
        st.write('Unique destinations:', len(numUnique_dest))
        numAirlines = ex.number_of_airlines('JFK')
        st.write('Airlines:', numAirlines)
        numModels = ex.number_of_models('JFK')
        st.write('Plane models:', numModels)
    with cols[2]:
        dest_list = ex.unique_arrive_airports_input('LGA')
        st.write('<p style="color:Green; font-size: 25px;">LGA</p>', unsafe_allow_html=True)
        # st.write('<p style="font-size: 12px;">La Guardia Airport</p>', unsafe_allow_html=True)
        st.write('Destinations:', len(dest_list))
        numUnique_dest = ex.unique_dest_input(dest_list)
        st.write('Unique destinations:', len(numUnique_dest))
        numAirlines = ex.number_of_airlines('LGA')
        st.write('Airlines:', numAirlines)
        numModels = ex.number_of_models('LGA')
        st.write('Plane models:', numModels)

c_4 = st.container(border=True)
    
with c_4:
    st.subheader('Average number of flights')
    
    cols = st.columns(2, gap='small')

    with cols[0]:
        scope = st.radio('Select a scope:', ('Month', 'Day', 'Hour'), horizontal=False)
    
    with cols[1]:
        avg_numFlights = ex.number_of_flights('EWR', scope, False)
        st.write(':blue[EWR]:', round(avg_numFlights))
        avg_numFlights = ex.number_of_flights('JFK', scope, False)
        st.write(':red[JFK]:', round(avg_numFlights))
        avg_numFlights = ex.number_of_flights('LGA', scope, False)
        st.write(':green[LGA]:', round(avg_numFlights))
    
    fig = ex.number_of_flights_graph(scope)
    st.plotly_chart(fig, use_container_width=True)        