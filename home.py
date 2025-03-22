import streamlit as st
import functions.extra as ex

st.set_page_config(page_title = 'Project Flights', 
                   layout = 'wide', 
                   initial_sidebar_state = 'expanded')

# st.sidebar.markdown(
#         """
#         <style>
#             [data-testid="stSidebarNav"]{
#                 background-image: url(https://www.google.com/url?sa=i&url=https%3A%2F%2Fvu.nl%2Fnl%2Fover-de-vu%2Fmeer-over%2Fhuisstijl&psig=AOvVaw1NbRQ1juYqf-dEq8n0jhca&ust=1742733567939000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCMiggczanYwDFQAAAAAdAAAAABAE);
#                 background-repeat: no-repeat;
#                 padding-top: 120px;
#                 background-position: 20px 20px;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

st.sidebar.page_link('home.py', label='Home Page', icon='🏠')
st.sidebar.page_link('pages/general.py', label='General Information', icon='ℹ️')    
st.sidebar.page_link('pages/delay.py', label='Delay Analysis', icon='⁉️')
st.sidebar.page_link('pages/interesting.py', label='Interesting Findings', icon='💡')

# home = st.Page('home.py', title='Home Page', icon='🏠')
# general = st.Page('pages/general.py', title='General Information', icon='ℹ️')    
# delay = st.Page('pages/delay.py', title='Delay Analysis', icon='⁉️')
# interest = st.Page('pages/interesting.py', title='Interesting Findings', icon='💡')

# pg = st.navigation([home, general, delay, interest])
# pg.run()

st.title('General Information of JFK airport')

st.header('Top 5 busiest routes')
    
c_1 = st.container(border=True)  
        
with c_1:
    result = ex.top_five_flights('JFK')
    fig = ex.printTopFiveFlights(list(result['origin']), list(result['dest']))
    
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
    st.dataframe(result_copy.set_index(result_copy.columns[0]), use_container_width=True)
        
st.header('Top 5 most used plane models')
    
c_3 = st.container(border=True)
    
with c_3:
    result = ex.top_five_planes_JFK()
    
    # cols = st.columns(3, gap = 'small')
    # with cols[0]:
    #     model = st.radio('Select a model:', set(result['model']))
    #     model_row = result.loc[result['model'] == model]
    # with cols[1]:
    #     st.write('Type:',model_row['type'].iloc[0])
    #     st.write('Number of engines:',model_row['engines'].iloc[0])
    #     st.write('Engine:',model_row['engine'].iloc[0])
    # with cols[2]:
    #     st.write('Speed:',model_row['speed'].iloc[0])
    #     st.write('Number of seats:',model_row['seats'].iloc[0])
    #     st.write('Number of planes:',model_row['numPlanes'].iloc[0])
        
    result_copy = result.copy()
    result_copy.columns = ['Type', 'Manufacturer', 'Model', 'Number of engines', 'Seats', 'Speed', 'Engine', 'Number of flights']
    st.dataframe(result_copy.set_index(result_copy.columns[0]), use_container_width=True)