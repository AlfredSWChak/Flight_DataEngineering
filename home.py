import streamlit as st
import alfred_function as af

st.set_page_config(page_title = 'Project Flights', 
                   layout = 'wide', 
                   initial_sidebar_state = 'expanded')

st.sidebar.page_link('home.py', label='Home')
st.sidebar.page_link('pages/part51.py', label='Lans Function')
st.sidebar.page_link('pages/alfred_dashboard.py', label='Alfreds Function')

st.text('Welcome, This is home page.')

st.header('Top 5 flights')
    
c_1 = st.container()
    
with c_1:
    airport = st.selectbox('Select a airport',['EWR', 'LGA', 'JFK', 'All airports'])
    button_clicked = st.button('Submit')
        
c_2 = st.container(border=True)  
        
with c_2:
    if button_clicked:
        result = af.top_five_flights(airport)
        st.table(result.set_index(result.columns[0]))
        
st.header('Top 5 plane models')
    
c_3 = st.container(border=True)
    
with c_3:
    result = af.top_five_planes()
    st.table(result.set_index(result.columns[0]))