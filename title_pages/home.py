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
    fig = ex.printN_NYC_airports()
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

# st.subheader('Top 5 busiest routes')

# c_1 = st.container(border=True)  
        
# with c_1:
#     result = ex.top_five_flights('JFK')
#     fig = ex.printTopFiveFlights(list(result['origin']), list(result['dest']))
    
#     fig.update_layout(title = f'Top 5 busiest routes departing from JFK')
#     fig.update_layout(geo_scope='usa', showlegend=False, dragmode=False)
#     fig.update_layout(hoverlabel_font_color='black', font_color = 'blue')
#     fig.update_traces(marker=dict(size=5, color='DarkSlateGrey'), textposition='top center')
#     # fig.update_annotations(bgcolor='black')
#     fig.update_coloraxes(showscale=False)
#     st.plotly_chart(fig, use_container_width=True)
    
#     result_copy = result.copy()
#     result_copy = result_copy.drop(columns=['origin'])
#     result_copy.columns = ['Destination Airport', 'Distance of flight (km)', 'Number of flights']
#     st.dataframe(result_copy.set_index(result_copy.columns[0]), use_container_width=True)
        
