import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import sqlite3

import part1 as pt1
import part3 as pt3
import part4 as pt4

import altair as alt
import alfred_function as af
import functions.airlines as alnes
import functions.flights as flt
import calendar
from datetime import datetime

# connection = sqlite3.connect('flights_database.db', check_same_thread=False)
# cursor = connection.cursor()

# def get_flight_data():
#     query = 'SELECT origin, dest, month, day, air_time, distance, carrier, tailnum, dep_delay FROM flights'
#     return pd.read_sql(query, connection)

# def get_airport_data():
#     query = 'SELECT faa, name FROM airports'
#     return pd.read_sql(query, connection)

# def main():
#     st.title('Flight Data Visualization')

#     flights_df = get_flight_data()
#     airports_df = get_airport_data()

#     origin_options = ['JFK', 'EWR', 'LGA']
#     origin = st.sidebar.selectbox("Select Departure Airport:", origin_options, key="origin_selectbox")
                                  
#     unique_dest_df = flights_df.groupby('dest')['origin'].nunique().reset_index()
#     unique_dest_df = unique_dest_df[unique_dest_df['origin'] == 1]

#     unique_dest_df = unique_dest_df[unique_dest_df['dest'].isin(flights_df[flights_df['origin'] == origin]['dest'].unique())]

#     if not unique_dest_df.empty:
#         st.subheader(f"Unique Destinations Served by {origin} Airport")
#         unique_dest_df['Frequency'] = unique_dest_df['dest'].apply(lambda x: f"{len(flights_df[flights_df['dest'] == x]) // 30} per month")
#         st.dataframe(unique_dest_df[['origin', 'dest', 'Frequency']])
#     else:
#         st.write("No unique destinations found for the selected origin.")

#     destination_options = flights_df['dest'].unique().tolist()
#     dest = st.sidebar.selectbox("Select Destination Airport:", destination_options)

#     filtered_df = flights_df[(flights_df['origin'] == origin) & (flights_df['dest'] == dest)]

#     if not filtered_df.empty:
#         st.subheader(f"Flight Statistics from {origin} to {dest}")
#         st.write(f"Total Flights: {len(filtered_df)}")
#         st.write(f"Average Weekly Flights: {len(filtered_df) / 52:.2f}")
#         st.write(f"Average Flight Time: {filtered_df['air_time'].mean():.2f} minutes")
#         st.write(f"Average Delay: {filtered_df['dep_delay'].mean():.2f} minutes")

#         place_counts = filtered_df['tailnum'].value_counts().head(5)
#         st.write("Most Used Aircraft Models:")
#         st.write(place_counts)

#     st.subheader("Top Destination Airports")
#     top_destinations = flights_df['dest'].value_counts().head(10)
#     st.bar_chart(top_destinations)

#     st.subheader("Unique Destination Analysis")
#     unique_dest_df = flights_df.groupby('dest')['origin'].nunique().reset_index()
#     unique_dest_df = unique_dest_df[unique_dest_df['origin'] == 1]
#     if not unique_dest_df.empty:
#         st.write("The following destinations are only served by one airport:")
#         st.write(unique_dest_df)
#     else:
#         st.write("No unique destination found.")

#     st.subheader("Flights per Month")
#     flights_per_month = flights_df['month'].value_counts().sort_index()
#     st.bar_chart(flights_per_month)

#     st.subheader("Total Delay per Month")
#     delay_per_month = flights_df.groupby('month')['dep_delay'].sum().sort_index()
#     st.bar_chart(delay_per_month)

#     origin_options = ['JFK', 'EWR', 'LGA']
#     origin = st.sidebar.selectbox("Select Departure Airport:", origin_options)
#     monthly_flights = flights_df.groupby(['origin', 'month']).size().unstack(fill_value = 0)
#     monthly_delay = flights_df.groupby(['origin', 'month'])['dep_delay'].sum().unstack(fill_value = 0)


# if __name__ == "__main__":
#     main()


st.sidebar.title('Functions')

options_set = ('Flight statistics for delay',
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

if add_selectbox == 'Flight statistics for delay':
    st.header('Flight Statistics for Delay')

    origin = st.selectbox('Select Departture Airport:', ['EWR', 'LGA', 'JFK'])
    destination_options = flt.get_all_destinations(origin)
    dest = st.selectbox('Select Destination Airport:', destination_options)

    flights_df = flt.get_flight_data()
    filtered_df = flights_df[(flights_df['origin'] == origin) & (flights_df['dest'] == dest)]

    if not filtered_df.empty:
        st.subheader(f"Flight Delay Statistics from {origin} to {dest}")
        st.write(f"Total Flights: {len(filtered_df)}")
        st.write(f"Average Weekly Flights: {len(filtered_df) / 52:.0f}")
        st.write(f"Average Flight Time: {filtered_df['air_time'].mean():.0f} minutes")
        st.write(f"Average Delay: {filtered_df['dep_delay'].mean():.0f} minutes")

        st.subheader(f"Flight per Month from {origin}")
        flights_per_month = filtered_df['month'].value_counts().sort_index()
        st.bar_chart(flights_per_month)

        st.subheader("Total Flights per Month for all airports")
        flights_per_month = flights_df['month'].value_counts().sort_index()
        st.bar_chart(flights_per_month)

        st.subheader(f"Total Delay per Month from {origin}")
        delay_per_month = filtered_df.groupby('month')['dep_delay'].sum().sort_index()
        st.bar_chart(delay_per_month)


        st.subheader("Total Delay per Month for all airports")
        delay_per_month = flights_df.groupby('month')['dep_delay'].sum().sort_index()
        st.bar_chart(delay_per_month)

    else:
        st.write("No flight data found for the selected route.")

elif add_selectbox == 'Delay analysis - Possible causes: Weather 🌦️':
    st.header('Delay analysis - Possible causes: Weather 🌦️')
    
    origin = st.selectbox('Select Departure Airport:',['EWR', 'LGA', 'JFK'])
    dest_list = sorted(pt3.unique_arrive_airports_input(origin))
    dest = st.selectbox('Select Arrival Airport:',dest_list)
    
    input_start_month = st.selectbox('Select the month of departure:',month_list)
    input_end_month = st.selectbox('Select the month of arrival:',month_list[month_list.index(input_start_month):])
    
    button_clicked = st.button('Select')
    
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

bkhm = st.sidebar.button("Back to home page", icon='🔙') 

if bkhm:
    st.switch_page("home.py")
