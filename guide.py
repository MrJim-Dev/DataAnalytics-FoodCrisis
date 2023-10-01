import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd


# df = pd.read_csv("./datasets/FoodInsecurity.pdf");

# philippines_data = df[df['Country'] == 'Philippines']
# philippines_data
# Sample Data
df = pd.DataFrame({
    'x': np.arange(10),
    'y': np.sin(np.arange(10)),
    'z': np.random.randn(10),
    'category': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
})

# Check if 'selected_plot' is already in the session state
if 'selected_plot' not in st.session_state:
    st.session_state.selected_plot = None

st.markdown("""
    <style>
        .stButton > button {
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)
# Sidebar navigation using buttons
st.sidebar.header("Choose a Plot Type")
plot_types = ["Scatter Plot", "Line Chart", "Bar Chart", "Histogram", "Pie Chart", "3D Scatter Plot", 
              "Box Plot", "Violin Plot", "Area Chart", "Sunburst Chart", "Polar Chart"]

for plot in plot_types:
    if st.sidebar.button(plot):
        st.session_state.selected_plot = plot

st.title(st.session_state.selected_plot if st.session_state.selected_plot else "Please select a plot from the sidebar")

# Display the corresponding plot based on the button clicked

if st.session_state.selected_plot == "Scatter Plot":
    fig = px.scatter(df, x='x', y='y', title='Scatter Plot')
    st.plotly_chart(fig)

elif st.session_state.selected_plot == "Line Chart":
    fig = px.line(df, x='x', y='y', title='Line Chart')
    st.plotly_chart(fig)

elif st.session_state.selected_plot == "Bar Chart":
    fig = px.bar(df, x='x', y='y', title='Bar Chart')
    st.plotly_chart(fig)

elif st.session_state.selected_plot == "Histogram":
    fig = px.histogram(df, x='y', title='Histogram')
    st.plotly_chart(fig)

elif st.session_state.selected_plot == "Pie Chart":
    fig = px.pie(df, values='y', names='x', title='Pie Chart')
    st.plotly_chart(fig)

elif st.session_state.selected_plot == "3D Scatter Plot":
    fig = px.scatter_3d(df, x='x', y='y', z='z', title='3D Scatter Plot')
    st.plotly_chart(fig)

elif st.session_state.selected_plot == "Box Plot":
    fig = px.box(df, x='category', y='y', title='Box Plot')
    st.plotly_chart(fig)

elif st.session_state.selected_plot == "Violin Plot":
    fig = px.violin(df, x='category', y='y', title='Violin Plot')
    st.plotly_chart(fig)

elif st.session_state.selected_plot == "Area Chart":
    fig = px.area(df, x='x', y='y', title='Area Chart')
    st.plotly_chart(fig)

elif st.session_state.selected_plot == "Sunburst Chart":
    df_sunburst = pd.DataFrame({
        'parents': ["", "A", "A", "B", "B"],
        'labels': ["Total", "A1", "A2", "B1", "B2"],
        'values': [10, 3, 7, 4, 6]
    })
    fig = px.sunburst(df_sunburst, names='labels', parents='parents', values='values', title='Sunburst Chart')
    st.plotly_chart(fig)

elif st.session_state.selected_plot == "Polar Chart":
    fig = px.line_polar(df, r='y', theta='x', title='Polar Chart')
    st.plotly_chart(fig)
