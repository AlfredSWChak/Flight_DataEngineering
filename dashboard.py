import streamlit as st
import alfred_function as af
import part3 as pt3

st.set_page_config(page_title = 'Project Flights', 
                   layout = 'wide', 
                   initial_sidebar_state = 'expanded')

st.sidebar.title('Functions')
home = st.sidebar.button('Home Page')

options_set = ('Flight statistics on specific day', 'Top five plane models')

add_selectbox = st.sidebar.radio('Options', 
                                 options=options_set, 
                                 label_visibility='hidden'
)

if home:
    st.text('Welcome, This is home page.')

elif add_selectbox == 'Flight statistics on specific day':
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
            
elif add_selectbox == 'Top five plane models':
    st.header('The top 5 plane models are:')
    
    c_1 = st.container(border=True)
    
    with c_1:
        result = af.top_five_planes()
        st.table(result.set_index(result.columns[0]))