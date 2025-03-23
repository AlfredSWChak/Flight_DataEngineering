import streamlit as st
import functions.flights as flt
import matplotlib.pyplot as plt

st.header('Flight Statistics for Delay')

origin = st.sidebar.selectbox('Select Departture Airport:', ['EWR', 'LGA', 'JFK'])
destination_options = flt.get_all_destinations(origin)
dest = st.sidebar.selectbox('Select Destination Airport:', destination_options)

flights_df = flt.get_flight_data()
filtered_df = flights_df[(flights_df['origin'] == origin) & (flights_df['dest'] == dest)]

if not filtered_df.empty:
    st.subheader(f"Flight Delay Statistics from {origin} to {dest}")
    st.write(f"Total Flights: {len(filtered_df)}")
    st.write(f"Average Weekly Flights: {len(filtered_df) / 52:.0f}")
    st.write(f"Average Flight Time: {filtered_df['air_time'].mean():.0f} minutes")
    st.write(f"Average Delay: {filtered_df['dep_delay'].mean():.0f} minutes")

    st.subheader(f"Flight per Month from {origin} to {dest}")
    flights_per_month = filtered_df['month'].value_counts().sort_index()
    st.bar_chart(flights_per_month)

    st.subheader("Total flights for three origin airports and the sum")
    filtered_df = flights_df
    flights_per_month = filtered_df.groupby(['month', 'origin']).size().unstack(fill_value=0)
    flights_per_month['Total'] = flights_per_month.sum(axis=1)
    fig, ax = plt.subplots()

    for airport in flights_per_month.columns:
        if airport != 'Total':
            ax.plot(flights_per_month.index, flights_per_month[airport], marker = 'o', linestyle = '-', label=f'{airport} airport')

    ax.plot(flights_per_month.index, flights_per_month['Total'], marker = 'x', linestyle = '-', color = 'blue', label = 'Total Flights')

    ax.set_xlabel("Month")
    ax.set_ylabel("Total Flights")
    ax.set_title("Total flight per Month")
    ax.legend(title = "Airport")

    st.pyplot(fig)

    st.subheader(f"Total Delay per Month from {origin} to {dest}")
    delay_per_month = filtered_df.groupby('month')['dep_delay'].sum().sort_index()
    st.bar_chart(delay_per_month)


    st.subheader("Total Delay per Month for all airports")
    delay_per_month = flights_df.groupby('month')['dep_delay'].sum().sort_index()
    st.bar_chart(delay_per_month)

else:
    st.write("No flight data found for the selected route.")