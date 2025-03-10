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
    origin = st.sidebar.selectbox("Select Departure Airport:", origin_options)

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

if __name__ == "__main__":
    main()


