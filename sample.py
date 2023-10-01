import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Title of the app
st.title("Food Prices Analysis for the Philippines")

# Read the dataset
data = pd.read_csv("D:\\School\\IT365 - Data Analytics\\1 Laboratory Activities\\data_analytics\\datasets\\02 global_food_prices.csv")

# Filter data for the Philippines and years 2008 and later
ph_data = data[(data['adm0_name'] == 'Philippines') & (data['mp_year'] >= 2008)].copy()

# Display ph_data (optional)
st.write(ph_data)

# Handle missing values 
numeric_columns = ph_data.select_dtypes(include=['float64', 'int64']).columns
ph_data[numeric_columns] = ph_data[numeric_columns].fillna(ph_data[numeric_columns].mean())

monthly_avg = ph_data.groupby(['mp_month', 'mp_year'])['mp_price'].mean().reset_index()
yearly_avg = ph_data.groupby('mp_year')['mp_price'].mean().reset_index()
market_monthly_avg = ph_data.groupby(['mp_month', 'mkt_name'])['mp_price'].mean().reset_index()

commodities = ['Fish', 'Meat', 'Potatoes', 'Onions', 'Tomatoes']

# Empty list to store data
averages = []

# Loop through each commodity to compute averages
for commodity in commodities:
    # Filter data based on keyword
    filtered_data = ph_data[ph_data['cm_name'].str.contains(commodity, case=False, na=False)]
    
    # Compute yearly average
    yearly_avg = filtered_data.groupby('mp_year')['mp_price'].mean().reset_index()
    yearly_avg['commodity'] = commodity
    
    # Append to the averages list
    averages.append(yearly_avg)

# Concatenate all the results
combined_avg = pd.concat(averages, ignore_index=True)

fig = px.line(combined_avg, 
              x='mp_year', 
              y='mp_price', 
              color='commodity', 
              title='Yearly Average Price of Commodities in the Philippines')
st.plotly_chart(fig)
