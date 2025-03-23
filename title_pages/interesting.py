import streamlit as st
import functions.extra as ex
import functions.manipulating as mp

st.sidebar.title('Features')

options_set = ('Flight statistics on a specific day',
               'Top five busiest routes',
               'Top five used plane models',
               'Top five popular airlines',
               'Unique destinations'
               )

add_selectbox = st.sidebar.radio('Options', 
                                 options=options_set, 
                                 label_visibility='hidden'
)

if add_selectbox == 'Flight statistics on a specific day':
    st.header('Flight statistics on a specific day')

    c_1 = st.container()
        
    with c_1:
        date = st.date_input('Select a date', value=None, min_value='2023-01-01', max_value='2023-12-31')
        
        temp = ex.getAirportFullName(['EWR', 'LGA', 'JFK'])
        joined_list = temp[['faa','name']].agg('-'.join, axis=1)
        
        selection = st.selectbox('Select an airport', sorted(joined_list))
        airport = selection[:3]
    
        button_clicked = st.button('Submit')
        
    c_2 = st.container(border=True)  
        
    with c_2:
        if button_clicked:
            
            month = date.month
            day = date.day
            
            numFlights, numUniqueDest, destMost, numMost =  mp.printStatisticsOnDateAtAirport(month, day, airport)
            
            st.text('On '+str(day)+'/'+str(month)+' at '+airport+', there are '+str(numFlights)+' flights.')
            st.text('On '+str(day)+'/'+str(month)+' at '+airport+', there are '+str(numUniqueDest)+' unique destinations.')
            st.text('On '+str(day)+'/'+str(month)+' at '+airport+', '+destMost+' is visited most often with '+str(numMost)+' flights.')
            
            fig = mp.printFlightsOnDateAtAirport(month, day, airport)
            fig.update_layout(showlegend=False, dragmode=False)
            fig.update_layout(hoverlabel_font_color='black', font_color = 'blue')
            fig.update_coloraxes(showscale=False)
            fig.update_traces(marker=dict(size=5, color='DarkSlateGrey'), textposition='top center')
            
            st.plotly_chart(fig, use_container_width=True)

elif add_selectbox == 'Top five busiest routes':
    st.header('Top FIVE busiest routes of selected airport')
    
    c_1 = st.container()
        
    with c_1:
        temp = ex.getAirportFullName(['EWR', 'LGA', 'JFK'])
        joined_list = temp[['faa','name']].agg('-'.join, axis=1)
        
        selection = st.selectbox('Select a departure airport', sorted(joined_list))
        airport = selection[:3]
        
        button_clicked = st.button('Submit')   
       
    c_2 = st.container(border=True)
        
    with c_2:   
        if button_clicked:
            result = ex.top_five_flights(airport)
            fig = ex.printTopFiveFlights(list(result['origin']), list(result['dest']))
            
            fig.update_layout(title = f'Top five flights of {airport}')
            fig.update_layout(geo_scope='usa', showlegend=False, dragmode=False)
            fig.update_layout(hoverlabel_font_color='black', font_color = 'blue')
            fig.update_coloraxes(showscale=False)
            fig.update_traces(marker=dict(size=5, color='DarkSlateGrey'), textposition='top center')
            
            st.plotly_chart(fig, use_container_width=True)
            
            result = result.drop(columns=['origin'])
            result.columns = ['Destination Airport', 'Distance of flight (km)', 'Number of flights']
            st.dataframe(result.set_index(result.columns[0]), use_container_width=True)

elif add_selectbox == 'Top five used plane models':
    st.header('Top FIVE most used plane models of selected airport')
    
    c_1 = st.container()
        
    with c_1:
        temp = ex.getAirportFullName(['EWR', 'LGA', 'JFK'])
        joined_list = temp[['faa','name']].agg('-'.join, axis=1)
        
        selection = st.selectbox('Select a departure airport', sorted(joined_list))
        airport = selection[:3]
        
        button_clicked = st.button('Submit')  
    
    c_2 = st.container(border=True)
        
    with c_2:   
        if button_clicked:   
            result = ex.top_five_planes(airport)
        
            result_copy = result.copy()
            result_copy.columns = ['Manufacturer', 'Model', 'Number of engines', 'Seats', 'Speed', 'Engine', 'Number of flights']
            st.dataframe(result_copy.set_index(result_copy.columns[0]), use_container_width=True)

elif add_selectbox == 'Top five popular airlines':
    st.header('Top FIVE most popular airlines of selected airport')
    
    c_1 = st.container()
        
    with c_1:
        temp = ex.getAirportFullName(['EWR', 'LGA', 'JFK'])
        joined_list = temp[['faa','name']].agg('-'.join, axis=1)
        
        selection = st.selectbox('Select a departure airport', sorted(joined_list))
        airport = selection[:3]
        
        button_clicked = st.button('Submit')   
       
    c_2 = st.container(border=True)
        
    with c_2:   
        if button_clicked:
            fig, result = ex.top_five_airlines(airport)
            result_copy = result.copy().head()
            result_copy.columns = ['Abbreviation', 'Full Name', 'Number of flights']
            st.dataframe(result_copy.set_index(result_copy.columns[0]), use_container_width=True)
            
            st.plotly_chart(fig, use_container_width=True)
            
elif add_selectbox == 'Unique destinations':
    st.header('Unique destinations departed from each airport')
    
    c_1 = st.container()
        
    with c_1:
        EWR_numUnique_dest, JFK_numUnique_dest, LGA_numUnique_dest, fig = ex.printUniqueDestinations()
        
        st.write(f':blue[EWR] has',len(EWR_numUnique_dest),f'unique destinations: {', '.join(sorted(EWR_numUnique_dest))}.')
        st.write(f':red[JFK] has',len(JFK_numUnique_dest),f'unique destinations: {', '.join(sorted(JFK_numUnique_dest))}.')
        st.write(f':green[LGA] has',len(LGA_numUnique_dest),f'unique destinations: {', '.join(sorted(LGA_numUnique_dest))}.')
    
    c_2 = st.container(border=True)
        
    with c_2:
        st.plotly_chart(fig, use_container_width=True)
            