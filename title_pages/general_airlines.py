import streamlit as st
import functions.airlines as alnes
            
st.header('General Information on airlines')

temp = alnes.getAirlines_list()
joined_df = temp[['carrier','name']].agg('-'.join, axis=1)

airline = st.sidebar.selectbox('Select an airline:', sorted(set(joined_df)))
airline_abbrv = airline[:2]
airline_fullName = airline[3:]
    
c_1 = st.container()

with c_1:
    unique_models_df, numOfPlanes, numOfUniqueModels, count_years_df, models_df = alnes.getAllTailnum(airline_abbrv)
    st.write(f':blue[{airline_fullName}] has total', numOfPlanes,'planes. ',numOfUniqueModels,'different models are provided.')
    
    manufacturer, model, numModel, year = alnes.getOldestModels(count_years_df)
    st.write(f'The oldest plane model in use is **{manufacturer}-{model}**. There are',numModel, 'models made in',str(year),'.')
        
    manufacturer, model, numModel, year = alnes.getYoungestModels(count_years_df)
    st.write(f'The youngest plane model in use is **{manufacturer}-{model}**. There are',numModel,'models made in',str(year),'.')
    
c_2 = st.container(border=True)

with c_2:    
    unique_models_df_copy = unique_models_df.copy()
    unique_models_df_copy.columns = ['Manufacturer', 'Model', 'Seats', 'Number of planes']
    st.dataframe(unique_models_df_copy.set_index(unique_models_df_copy.columns[0]), use_container_width=True)
    
    scope = st.radio('Select a scope:', ('Model', 'Manufacturer', 'Year'), horizontal=True)
    
    fig = alnes.getModelStatistics(scope, unique_models_df, models_df)
    fig.update_layout(legend=dict(title=dict(text=scope, font_color='grey')))
    
    st.plotly_chart(fig, use_container_width=True)    