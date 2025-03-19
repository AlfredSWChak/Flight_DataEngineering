import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import sqlite3

import part1 as pt1
import part3 as pt3
import part4 as pt4

connection = sqlite3.connect('flights_database.db')
cursor = connection.cursor()

def get_flight_data():
    query = 'SELECT origin, dest, month, day, air_time, distance, carrier, tailnum, dep_delay FROM flights'
    return pd.read_sql(query, connection)

def get_airport_data():
    query = 'SELECT faa, name FROM airports'
    return pd.read_sql(query, connection)

def main():
    st.title('Flight Data Visualization')

    flights_df = get_flight_data()
    airports_df = get_airport_data()

    origin_options = ['JFK', 'EWR', 'LGA']
    origin = st.sidebar.selectbox("Select Departure Airport:", origin_options, key="origin_selectbox")
                                  
    unique_dest_df = flights_df.groupby('dest')['origin'].nunique().reset_index()
    unique_dest_df = unique_dest_df[unique_dest_df['origin'] == 1]

    unique_dest_df = unique_dest_df[unique_dest_df['dest'].isin(flights_df[flights_df['origin'] == origin]['dest'].unique())]

    if not unique_dest_df.empty:
        st.subheader(f"Unique Destinations Served by {origin} Airport")
        unique_dest_df['Frequency'] = unique_dest_df['dest'].apply(lambda x: f"{len(flights_df[flights_df['dest'] == x]) // 30} per month")
        st.dataframe(unique_dest_df[['origin', 'dest', 'Frequency']])
    else:
        st.write("No unique destinations found for the selected origin.")

    destination_options = flights_df['dest'].unique().tolist()
    dest = st.sidebar.selectbox("Select Destination Airport:", destination_options)

    filtered_df = flights_df[(flights_df['origin'] == origin) & (flights_df['dest'] == dest)]

    if not filtered_df.empty:
        st.subheader(f"Flight Statistics from {origin} to {dest}")
        st.write(f"Total Flights: {len(filtered_df)}")
        st.write(f"Average Weekly Flights: {len(filtered_df) / 52:.2f}")
        st.write(f"Average Flight Time: {filtered_df['air_time'].mean():.2f} minutes")
        st.write(f"Average Delay: {filtered_df['dep_delay'].mean():.2f} minutes")

        place_counts = filtered_df['tailnum'].value_counts().head(5)
        st.write("Most Used Aircraft Models:")
        st.write(place_counts)

    st.subheader("Top Destination Airports")
    top_destinations = flights_df['dest'].value_counts().head(10)
    st.bar_chart(top_destinations)

    st.subheader("Unique Destination Analysis")
    unique_dest_df = flights_df.groupby('dest')['origin'].nunique().reset_index()
    unique_dest_df = unique_dest_df[unique_dest_df['origin'] == 1]
    if not unique_dest_df.empty:
        st.write("The following destinations are only served by one airport:")
        st.write(unique_dest_df)
    else:
        st.write("No unique destination found.")

    st.subheader("Flights per Month")
    flights_per_month = flights_df['month'].value_counts().sort_index()
    st.bar_chart(flights_per_month)

    st.subheader("Total Delay per Month")
    delay_per_month = flights_df.groupby('month')['dep_delay'].sum().sort_index()
    st.bar_chart(delay_per_month)

    origin_options = ['JFK', 'EWR', 'LGA']
    origin = st.sidebar.selectbox("Select Departure Airport:", origin_options)
    monthly_flights = flights_df.groupby(['origin', 'month']).size().unstack(fill_value = 0)
    monthly_delay = flights_df.groupby(['origin', 'month'])['dep_delay'].sum().unstack(fill_value = 0)

    st.subheader(f"Flights per Month")
    st.bar_chart(monthly_flights)

    st.subheader(f"Total Delay per Month")
    st.bar_chart(monthly_delay)

if __name__ == "__main__":
    main()

bkhm = st.sidebar.button("Back to home page", icon='🔙') 

if bkhm:
    st.switch_page("home.py")
