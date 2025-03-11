import streamlit as st

st.set_page_config(page_title = 'Project Flights', 
                   layout = 'wide', 
                   initial_sidebar_state = 'expanded')

st.sidebar.page_link('home.py', label='Home')
st.sidebar.page_link('pages/part51.py', label='Lans Function')
st.sidebar.page_link('pages/alfred_dashboard.py', label='Alfreds Function')

st.text('Welcome, This is home page.')