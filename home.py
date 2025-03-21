import streamlit as st
import alfred_function as af
import part1 as pt1
import functions.weather as wthr

st.set_page_config(page_title = 'Project Flights', 
                   layout = 'wide', 
                   initial_sidebar_state = 'expanded')

st.sidebar.page_link('home.py', label='Home Page', icon='🏠')
st.sidebar.page_link('pages/general.py', label='General Information', icon='ℹ️')
st.sidebar.page_link('pages/delay.py', label='Delay Analysis', icon='⁉️')

st.title('General Information of JFK airport')

st.header('Top 5 busiest routes')
    
c_1 = st.container(border=True)  
        
with c_1:
    result = af.top_five_flights('JFK')
    fig = af.printTopFiveFlights(list(result['origin']), list(result['dest']))
    
    fig.update_layout(title = f'Top 5 busiest routes departing from JFK')
    fig.update_layout(geo_scope='usa', showlegend=False, dragmode=False)
    fig.update_layout(hoverlabel_font_color='black', font_color = 'blue')
    fig.update_traces(marker=dict(size=5, color='DarkSlateGrey'), textposition='top center')
    # fig.update_annotations(bgcolor='black')
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(fig, use_container_width=True)
    
    result_copy = result.copy()
    result_copy = result_copy.drop(columns=['origin'])
    result_copy.columns = ['Destination Airport', 'Distance of flight (km)', 'Number of flights']
    # st.table(result_copy.set_index(result_copy.columns[0]))
    st.dataframe(result_copy.set_index(result_copy.columns[0]), use_container_width=True)
        
st.header('Top 5 most used plane models')
    
c_3 = st.container(border=True)
    
with c_3:
    result = af.top_five_planes()
    
    cols = st.columns(3, gap = 'small')
    with cols[0]:
        model = st.radio('Select a model:', set(result['model']))
        model_row = result.loc[result['model'] == model]
    with cols[1]:
        st.write('Type:',model_row['type'].iloc[0])
        st.write('Number of engines:',model_row['engines'].iloc[0])
        st.write('Engine:',model_row['engine'].iloc[0])
    with cols[2]:
        st.write('Speed:',model_row['speed'].iloc[0])
        st.write('Number of seats:',model_row['seats'].iloc[0])
        st.write('Number of planes:',model_row['numPlanes'].iloc[0])
        
    result_copy = result.copy()
    # result_copy.columns = result_copy.columns.str.upper()
    result_copy.columns = ['Type', 'Manufacturer', 'Model', 'Number of engines', 'Seats', 'Speed(m/s)', 'Engine', 'Number of planes']
    # st.table(result_copy.set_index(result_copy.columns[0]))
    st.dataframe(result_copy.set_index(result_copy.columns[0]), use_container_width=True)

    
st.header('General Information about weather at JFK')

c_2 = st.container()
        
with c_2:
    cols = st.columns((4, 4), gap = 'medium')
    
    with cols[0]:
        season = st.radio('Select a season:', ('Whole year', 'Spring (March, April, May)', 'Summer (June, July, August)', 'Autumn (September, October, November)', 'Winter (December, Janurary, Feburary)'), horizontal=False)
        month_list = wthr.getMonth(season)
        
    with cols[1]:
        fig, result = wthr.hourlyAverage(month_list)
        st.write(f'***Average*** of {season}')
        st.write('Wind Speed:',round(result['wind_speed'],3),'m/s')
        st.write('Wind Gust:',round(result['wind_gust'],3), 'm/s')
        st.write('Visibility:',round(result['visib'],3),'m')     

c_4 = st.container(border=True)
    
with c_4:
    st.plotly_chart(fig, use_container_width=True)
