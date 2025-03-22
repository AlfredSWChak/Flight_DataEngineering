import streamlit as st
import functions.extra as ex

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