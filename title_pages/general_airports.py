import streamlit as st
import functions.extra as ex
import functions.manipulating as mp
import functions.airlines as alnes

st.header('General Information of airports')

c_1 = st.container(border=True)
    
with c_1:
    area = st.radio('Select a scope:', ('World', 'USA'
                                        # , 'Europe', 'Asia', 'Africa', 'North America', 'South America'
                                        ), horizontal=True)
    
    fig = alnes.showAllAirports()
    fig.update_layout(geo_scope=area.lower(), dragmode=False)
    st.plotly_chart(fig, use_container_width=True)
    
st.subheader('Airport General Information')

c_2 = st.container()

with c_2:
    airport_df = mp.getTable('airports')
    temp = mp.getAirportsListInfo(airport_df['faa'])
    joined_list = temp[['faa','name']].agg('-'.join, axis=1)
    
    selection = st.sidebar.selectbox('Select an Airport:', joined_list)
    airport = selection[:3]
    
    cols = st.columns(2, gap = 'small')
    
    with cols[0]:
        airport_row = mp.getAirportInfo(airport)
        st.write(f'Full name: :blue[{airport_row['name'][0]}]')
        st.write(f'Daylight Savings Time zone: {ex.getDSTMeaning(airport_row['dst'][0])}')
        st.write('Time Zone: GMT',airport_row['tz'][0])
    
    with cols[1]:
        airport_row = mp.getAirportInfo(airport)
        st.write('Latitude: ',airport_row['lat'][0],'°')
        st.write('Longitude: ',airport_row['lon'][0],'°')
        st.write('Altitude: ',airport_row['alt'][0],'m')
        
c_3 = st.container(border=True)

with c_3: 
    unique_origin = mp.unique_depart_airports_input(airport)
    
    if (len(unique_origin) == 0):
        st.write(f'There are :red[NO FLIGHTS] depart from NYC airports to :blue[{selection}].')
    elif (len(unique_origin) == 1):
        st.write(f':blue[{selection}] can be travelled from: **{unique_origin[0]}**.')
    elif (len(unique_origin) == 2):
        st.write(f':blue[{selection}] can be travelled from: **{unique_origin[0]}** and **{unique_origin[1]}**.')
    elif (len(unique_origin) == 3):
        st.write(f':blue[{selection}] can be travelled from: **{unique_origin[0]}**, **{unique_origin[1]}** and **{unique_origin[2]}**.')
    
    fig = ex.printOneAirport(airport)
    fig.update_layout(dragmode=False)
    st.plotly_chart(fig, use_container_width=True)