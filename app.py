import pandas as pd
import streamlit as st
import plotly.express as px
import pycountry
import numpy as np
st.set_page_config(layout="wide", initial_sidebar_state="expanded", )


#load dataset
covid = pd.read_csv('COVID-19.csv')

st.sidebar.header('Covid-19 Dashboard')

menu = ['New_cases', 'Cumulative_cases', 'New_deaths', 'Cumulative_deaths']
selection= st.sidebar.selectbox('Choose One', menu)
st.sidebar.write('Covid-19 Dashboard is a visualization of data related to Covid-19 pandemic. The dashboard present information on numbers of confirmed cases and deaths. Based on the selection the numbers are presented on a daily level or cumulatively over time across the world.')

def get_iso3(iso2):
    try:
        return pycountry.countries.get(alpha_2=iso2).alpha_3
    except:
        pass

covid['iso_alpha'] = covid.Country_code.apply(lambda x: get_iso3(x))

covid['cases'] = covid['New_cases'].cumsum() # creating hover data for all cases
covid['deaths'] = covid['New_deaths'].cumsum() # creating hover data for all deaths

# creating hover data for daily growth rate in cases
covid['Cases_change'] = covid['Cumulative_cases'] - covid['Cumulative_cases'].shift(1) 
# creating hover data for daily percentage growth rate in cases
covid['Cases_Daily_change'] = np.round(covid['Cumulative_cases'].pct_change()*100, 2).astype(str) + '%'

# creating hover data for daily growth rate in deaths
covid['Death_change'] = covid['Cumulative_deaths'] - covid['Cumulative_deaths'].shift(1)
# creating hover data for daily percentage growth rate in deaths
covid['Death_Daily_change'] = np.round(covid['Cumulative_deaths'].pct_change()*100, 2).astype(str) + '%'



# creating a select options for analysis & visualization in choropleth
if selection== 'New_cases':
    st.header('Covid New Cases')
    fig = px.choropleth(covid, locations = 'iso_alpha', 
    color = 'New_cases', 
    animation_frame = 'Date_reported',
    color_continuous_scale=px.colors.sequential.Peach,
    hover_name = 'Country', 
    hover_data = ['Cumulative_cases', 'New_deaths', 'Cumulative_deaths'])
elif selection== 'Cumulative_cases':
    st.header('Covid Cumulative Cases')
    fig = px.choropleth(covid, locations = 'iso_alpha', 
    color = 'Cumulative_cases', 
    animation_frame = 'Date_reported',
    color_continuous_scale=px.colors.sequential.Mint,
    hover_name = 'Country', 
    hover_data = ['New_cases', 'New_deaths', 'Cumulative_deaths'])
elif selection == 'New_deaths':
    st.header('Covid New Deaths')
    fig = px.choropleth(covid, locations = 'iso_alpha', 
    color = 'New_deaths', 
    animation_frame = 'Date_reported',
    color_continuous_scale=px.colors.sequential.Peach,
    hover_name = 'Country', 
    hover_data = ['New_cases', 'Cumulative_cases', 'Cumulative_deaths'])
else:
    st.header('Covid Cumulative Deaths')
    fig = px.choropleth(covid, locations = 'iso_alpha', 
    color = 'Cumulative_deaths', 
    animation_frame = 'Date_reported',
    color_continuous_scale=px.colors.sequential.Mint,
    hover_name = 'Country')
    # st.sidebar.markdown('_Highest cumulative deaths are from:_')
    # st.sidebar.write(['Unites states; 1M, Brazil; 694K, India; 530k'])
    # hover_data = ['New_cases', 'Cumulative_cases']
fig.update_layout(height=550) 
st.plotly_chart(fig, use_container_width=True, theme='streamlit')


#Bar graphs for cumulative cases & deaths
col1, col2 = st.columns(2)

with col1:
    st.header('Cumulative Cases per Day Overview')
    fig2 = px.bar(covid, x = 'Date_reported', y = 'Cumulative_cases', hover_data = ['cases', 'Cases_change', 'Cases_Daily_change'], title = 'Cumulative Cases')
    fig2.update_layout(400)
    st.plotly_chart(fig2, use_container_width=True, theme='streamlit')

with col2:
    st.header('Cumulative Deaths per Day Overview')
    fig3 = px.bar(covid, x = 'Date_reported', y = 'Cumulative_deaths', hover_data = ['deaths', 'Death_change', 'Death_Daily_change'], title = 'Cumulative deaths')
    fig3.update_layout(400)
    st.plotly_chart(fig3, use_container_width=True, theme='streamlit')


