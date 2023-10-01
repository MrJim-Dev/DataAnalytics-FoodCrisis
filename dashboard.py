import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd


# Check if 'selected_menu' is already in the session state
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Introduction"

# Style the buttons to make them full-width and add styling for custom metric container
st.markdown("""
    <style>
        .stButton > button {
            width: 100%;
        }

        .customMetric {
            background-color: #f0f0f0;
            border-radius: 10px;
            padding: 20px;
            margin: 1%;
            font-size: 1.2em;
            text-align: center;
            width: 48%;  /* Adjusted to 50% width */
            float: left;  /* Make them float left */
        }

        .customMetric h2 {
            color: black;
            font-weight: bold;
            margin: 0;
            padding: 0;
        }

        .customMetric p {
            color: black;
        }

        .customMetric label {
            color: #888;
            font-size: 0.9em;
            display: block;
            margin-top: 10px;
        }

    </style>
""", unsafe_allow_html=True)

# Sidebar navigation using buttons
menu_options = ["Introduction", "Food Prices", "Food Security", "Children Nourishment", "Conclusions"]

for menu in menu_options:
    if st.sidebar.button(menu):
        st.session_state.selected_menu = menu

# Display content based on selected menu
if st.session_state.selected_menu == "Introduction":
    # Load the dataset
    df = pd.read_csv("datasets/01 global-hunger-index.csv")

    # Filter data for the Philippines
    philippines_data = df[df['Entity'] == 'Philippines']

    st.header("Stating the Problem")
    st.write("The Philippines, despite its agricultural potential, holds a concerning rank on the Global Hunger Index⁴, signaling a deep-seated issue with hunger and food access. This challenge extends from fields to urban centers, affecting its vast population in myriad ways. By examining key datasets that encompass food prices, security, and child malnutrition indicators, we aim to paint a comprehensive picture of the nation's food crisis. Our presentation's insights will serve as a crucial resource, providing a foundation for strategies that address the root causes and pave the way for a food-secure Philippines.")

    metrics_html = ""  # Collecting metrics HTML in this string

    metrics_html += f"""
    <div class="customMetric">
        <p>Hunger Index</p>
        <h2>16.8</h2>
        <label>Year 2021</label>
    </div>
    """

    metrics_html += f"""
    <div class="customMetric">
        <p>Food Security Index</p>
        <h2>59.3</h2>
        <label>Year 2022</label>
    </div>
    """

    # Render the metrics
    st.markdown(metrics_html, unsafe_allow_html=True)

    
    st.image('images/ghi-scale.png', caption='Global Hunger Index Severity Scale', use_column_width=True)


    selected_countries = ["Albania", "Indonesia", "Malaysia", "Philippines", "Thailand", "Vietnam", "Russia", "Turkey", "China"]
    df_filtered = df[df['Entity'].isin(selected_countries)]

    df_2021_filtered = df_filtered[df_filtered['Year'] == 2021]
    fig_bar = px.bar(df_2021_filtered, x='Entity', y='Global Hunger Index (2021)', title='Global Hunger Index for Selected Countries in 2021')

    st.plotly_chart(fig_bar)

elif st.session_state.selected_menu == "Food Prices":
    # Header and Description
    st.header("Food Prices")
    st.write("This section presents a detailed examination of the evolving price trends of key food commodities in the Philippines, with an emphasis on rice and maize. Through these visual data plots, we highlight the price trajectories and market dynamics over time. Such insights are essential to understand the economic forces at play, the accessibility of staple foods for the population, and potential areas of intervention to ensure food affordability.")

    # Load Data
    food_prices = pd.read_csv("datasets/02 global_food_prices.csv")

    # Filter data for the Philippines and limit to 2020
    food_prices_phil = food_prices[(food_prices["adm0_name"] == "Philippines") & (food_prices["mp_year"] <= 2020)]

    # Commodity specific plots
    commodities = ["Rice", "Maize"]

    for commodity in commodities:
        filtered_prices = food_prices_phil[food_prices_phil['cm_name'].str.contains(commodity)]
        mean_prices = filtered_prices.groupby(['mp_year', 'cm_name', 'pt_name'])['mp_price'].mean().reset_index()
        
        # Check if there's data for or before 2020 for this commodity
        if 2020 not in mean_prices['mp_year'].values:
            continue  # Skip the rest of the loop and move on to the next commodity
        
        fig = px.line(mean_prices, x="mp_year", y="mp_price", color="cm_name",
                    title=f"Average Price of {commodity} Commodities in Philippines Over Time",
                    labels={"mp_year": "Year", "mp_price": "Average Price", "cm_name": commodity + " Commodities"})


        for trace in fig.data:
            if "Wholesale" not in trace.name and "Retail" not in trace.name:
                trace.visible = 'legendonly'

        st.plotly_chart(fig)

    # Average Price of commodities starting from 2008
    filtered_phil_data = food_prices_phil[food_prices_phil['mp_year'] >= 2008].copy()

    # Handle missing values using Interpolation
    filtered_phil_data['mp_price'] = filtered_phil_data['mp_price'].interpolate(method='linear')

    commodities = ['Fish', 'Meat', 'Potatoes', 'Onions', 'Tomatoes']
    averages = []

    for commodity in commodities:
        filtered_data = filtered_phil_data[filtered_phil_data['cm_name'].str.contains(commodity, case=False, na=False)]
        yearly_avg = filtered_data.groupby('mp_year')['mp_price'].mean().reset_index()
        yearly_avg['commodity'] = commodity
        averages.append(yearly_avg)

    combined_avg = pd.concat(averages, ignore_index=True)
    fig = px.line(combined_avg, x='mp_year', y='mp_price', color='commodity', title='Yearly Average Price of Commodities in the Philippines starting from 2008',
    labels={"mp_year": "Year", "mp_price": "Average Price", "commodity": "Commodities"})
    st.plotly_chart(fig)


    # You can add visualizations related to Food Prices here

elif st.session_state.selected_menu == "Food Security":
    st.header("Food Security")
    st.write("This visual representation offers insights into the multi-faceted dimensions of food security across selected nations. Through the radar chart, we decode factors like affordability, availability, and sustainability, making it easier to understand where each country stands. It serves as a tool for policymakers and stakeholders to pinpoint areas of improvement and recognize strengths in food security strategies.")
    # You can add visualizations related to Food Security here

    # Read the data from a CSV file
    food_security_df = pd.read_csv("datasets/03 Global Food Security Index 2022.csv")

    # Define the countries you want to include in the radar chart
    countries_to_include = ['Albania', 'China', 'Indonesia', 'Malaysia', 'Philippines', 'Russia', 'Thailand', 'Turkey', 'Vietnam']

    # Filter the data to include only the selected countries
    filtered_food_data = food_security_df[food_security_df['Country'].isin(countries_to_include)]

    # Reshape the data for the radar chart
    reshaped_food_data = pd.melt(
        filtered_food_data,
        id_vars=['Country'],
        value_vars=['Affordability', 'Availability', 'Quality and Safety', 'Sustainability and Adaptation', 'Overall score'],
        var_name='Category',
        value_name='Score'
    )

    # Sort the data by 'Category' for better visualization
    reshaped_food_data = reshaped_food_data.sort_values(by='Category')

    # Create a radar chart with adjusted interval starting from 40
    fig = px.line_polar(
        reshaped_food_data,
        r='Score',
        theta='Category',
        line_close=True,
        color='Country',
        title='Radar Chart of Actual Values',
        template='plotly_dark',
    )

    # Adjust the interval on the radial axis starting from 40
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                tickvals=list(range(40, 101, 5)),  # Adjust the tick values starting from 40 at intervals of 5
                ticktext=list(range(40, 101, 5)),  # Display the tick values
            )
        )
    )

    # Show the chart
    st.plotly_chart(fig)


elif st.session_state.selected_menu == "Children Nourishment":
    st.header("Children Nourishment")
    st.write("This page presents a comprehensive analysis of child nourishment trends over the years, focusing on underweight, stunting, and wasting metrics. Through these visual representations, we aim to shed light on the nutritional challenges faced by children in various countries, emphasizing the need for targeted interventions and policies.")

    # The given code uses a similar procedure for underweight, stunting, and wasting data. 
    # I will replace the bar plots with line plots for each of these metrics.

    metrics = [
        {
            'file': 'datasets/share-of-children-with-a-weight-too-low-for-their-height-wasting.csv',
            'value_name': 'Prevalence of wasting, weight for height (% of children under 5)',
            'plot_title': 'Underweight Trends Over Time',
            'y_axis_title': 'Underweight'
        },
        {
            'file': 'datasets/share-of-children-younger-than-5-who-suffer-from-stunting.csv',
            'value_name': 'Prevalence of stunting, height for age (% of children under 5)',
            'plot_title': 'Stunting Trends Over Time',
            'y_axis_title': 'Stunting'
        },
        {
            'file': 'datasets/share-of-children-with-a-weight-too-low-for-their-height-wasting.csv',
            'value_name': 'Prevalence of wasting, weight for height (% of children under 5)',
            'plot_title': 'Wasting Trends Over Time',
            'y_axis_title': 'Wasting'
        }
    ]

    for metric in metrics:
        # Read the CSV file
        df = pd.read_csv(metric['file'])

        # List of countries you want to include in the plot
        selected_countries = ['China', 'Malaysia', 'Russia', 'Vietnam', 'Turkey', 'Indonesia', 'Thailand', 'Philippines']

        # Filter data for selected countries
        filtered_data = df[df['Entity'].isin(selected_countries)]

        # Pivot the filtered data
        pivot_filtered_data = filtered_data.pivot_table(
            values=metric['value_name'],
            index='Entity',
            columns='Year'
        )

        # Fill missing values using linear regression and other processing (retained from the original code)
        coefficients_df = pd.DataFrame(index=filtered_data['Entity'].unique(), columns=['Intercept', 'Coefficient'])

        for country in filtered_data['Entity'].unique():
            country_data = filtered_data[filtered_data['Entity'] == country]
            X = country_data['Year'].values.reshape(-1, 1)
            y = country_data[metric['value_name']].values

            model = LinearRegression()
            model.fit(X, y)

            coefficients_df.loc[country, 'Intercept'] = model.intercept_
            coefficients_df.loc[country, 'Coefficient'] = model.coef_[0]

        for i in range(len(pivot_filtered_data)):
            country = pivot_filtered_data.index[i]
            intercept = coefficients_df.loc[country, 'Intercept']
            coefficient = coefficients_df.loc[country, 'Coefficient']
            missing_values = pivot_filtered_data.iloc[i].isnull()
            years = missing_values.index
            predicted_values = intercept + coefficient * years
            pivot_filtered_data.loc[country, years] = pivot_filtered_data.loc[country, years].combine_first(pd.Series(predicted_values, index=years))

        pivot_filtered_data[pivot_filtered_data < 0] = 0

        # Reset the index for the plot
        pivot_filtered_data_reset = pivot_filtered_data.reset_index()

        # Melt the DataFrame for plotting
        melted_data = pd.melt(pivot_filtered_data_reset, id_vars=['Entity'], var_name='Year', value_name='Metric Value')

        # Plot the data using Plotly Express LINE PLOT
        fig = px.line(melted_data, x='Year', y='Metric Value', color='Entity',
                    title=metric['plot_title'],
                    labels={'Metric Value': 'Metric Value', 'Entity': 'Country', 'Year': 'Year'})

        # Update layout for better readability
        fig.update_layout(xaxis_title='Year', yaxis_title=metric['y_axis_title'])

        # Show the plot
        st.plotly_chart(fig)




elif st.session_state.selected_menu == "Conclusions":
    st.header("Conclusions")
    st.write("This section wraps up the findings and discusses the next steps and recommendations.")
