import streamlit as st

# st.sidebar.markdown(
#         """
#         <style>
#             [data-testid="stSidebarNav"] {
#                 background-image: url(https://vu.nl/nl);
#                 background-repeat: no-repeat;
#                 padding-top: 120px;
#                 background-position: 20px 20px;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# st.set_page_config(page_title = 'Project Flights', 
#                    layout = 'wide', 
#                    initial_sidebar_state = 'expanded')

home = st.Page('title_pages/home.py', title='Flights from NYC', icon='🗽')
general_airlines = st.Page('title_pages/general_airlines.py', title='Airlines', icon='🛩️')
general_airports = st.Page('title_pages/general_airports.py', title='Airports', icon='🗺️')
general_flights = st.Page('title_pages/general_flights.py', title='Flights', icon='🛫')
general_weather = st.Page('title_pages/general_weather.py', title='Weather', icon='🌤️')
delay_flights = st.Page('title_pages/delay_flights.py', title='Flights Statistics', icon='📉')
delay_weather = st.Page('title_pages/delay_weather.py', title='Possible causes', icon='💭')
interest = st.Page('title_pages/interesting.py', title='Interesting Findings', icon='💡')

pg = st.navigation({'🏠 Home': [home], 
                    'ℹ️ General Information': [general_airlines, general_airports, general_flights, general_weather], 
                    '⁉️ Delay Analysis': [delay_flights, delay_weather], 
                    '📍 Others': [interest]})
pg.run()