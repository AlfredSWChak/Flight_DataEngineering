import streamlit as st
import alfred_function as af
import part1 as pt1

st.set_page_config(page_title = 'Project Flights', 
                   layout = 'wide', 
                   initial_sidebar_state = 'expanded')

st.sidebar.page_link('home.py', label='Home')
st.sidebar.page_link('pages/part51.py', label='Lans Function')
st.sidebar.page_link('pages/alfred_dashboard.py', label='Alfreds Function')

st.text('Welcome, This is home page.')

c_4 = st.container(border=True)
    
with c_4:
    fig = pt1.showAllAirports()
    area = st.radio('Select a scope:', ('World', 'USA', 'Europe', 'Asia', 'Africa', 'North America', 'South America'), horizontal=True)
    fig.update_layout(geo_scope=area.lower())
    st.plotly_chart(fig, use_container_width=True)

st.header('Top 5 flights')
    
c_1 = st.container()
    
with c_1:
    airport = st.selectbox('Select a airport',['EWR', 'LGA', 'JFK', 'All airports'])
    button_clicked = st.button('Submit')
        
c_2 = st.container(border=True)  
        
with c_2:
    if button_clicked:
        result = af.top_five_flights(airport)
        fig = af.printTopFiveFlights(list(result['origin']), list(result['dest']))
        
        fig.update_layout(geo_scope='usa')
        fig.update_layout(title = f'Top five flights of {airport}')
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        # st.table(result.set_index(result.columns[0]))
        
st.header('Top 5 plane models')
    
c_3 = st.container(border=True)
    
with c_3:
    result = af.top_five_planes()
    
    # model = st.radio('Select a model:', set(result['model']))
    # model_row = result.loc[result['model'] > model]
    
    cols = st.columns((4, 4, 4), gap = 'medium')
    with cols[0]:
        model = st.radio('Select a model:', set(result['model']))
        model_row = result.loc[result['model'] > model]
    with cols[1]:
        st.write('Type:',model_row['type'].iloc[0])
        st.write('Number of engines:',model_row['engines'].iloc[0])
        st.write('Engine:',model_row['engine'].iloc[0])
    with cols[2]:
        st.write('Speed:',model_row['speed'].iloc[0])
        st.write('Number of seats:',model_row['seats'].iloc[0])
        st.write('Number of planes:',model_row['numPlanes'].iloc[0])
   
    st.table(result.set_index(result.columns[0]))