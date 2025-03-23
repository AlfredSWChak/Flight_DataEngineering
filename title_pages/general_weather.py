import streamlit as st
import functions.weather as wthr
import functions.manipulating as mp
import calendar

month_list = list(calendar.month_name)[1:]

st.header('General Information about weather')

c_1 = st.container(border=True)
        
with c_1:
    temp = mp.getAirportsListInfo(['EWR', 'LGA', 'JFK'])
    joined_list = temp[['faa','name']].agg('-'.join, axis=1)
    
    selection = st.sidebar.selectbox('Select an airport', sorted(joined_list))
    airport = selection[:3]
    
    cols = st.columns((4, 4), gap = 'medium')
    
    with cols[0]:
        season = st.radio('Select a season:', ('Spring (March, April, May)', 'Summer (June, July, August)', 'Autumn (September, October, November)', 'Winter (December, Janurary, Feburary)'), horizontal=False)
        
    with cols[1]:
        month_list = wthr.getMonth(season)
        fig, result = wthr.hourlyAverage(airport, month_list)
        
        st.write('**Average**:')
        st.write('Wind Speed:',round(result['wind_speed'],3),'m/s')
        st.write('Wind Gust:',round(result['wind_gust'],3), 'm/s')
        st.write('Visibility:',round(result['visib'],3),'m')     

    st.plotly_chart(fig, use_container_width=True)