import pandas as pd
import scipy.stats
import streamlit as st
import time
from matplotlib import pyplot as plt
import plotly.express as px

# Load the data file into a DataFrame
data = pd.read_csv('vehicles_us.csv', sep=',')

# Convert `model_year` from a float to int
data['model_year'] = data['model_year'].dropna().astype(int)

# Page heading
st.header('Vehicle Ads Plot Page')
st.header('Choose the type of charts needed')

# Create checkboxes
show_histogram = st.checkbox('Show Histograms')
show_scatter = st.checkbox('Show Scatter Plots')

# Display histograms if option is checked
if show_histogram:
    st.header('Vehicle Ads - Histograms for Model Year and Price')

    # Histogram for `model_year`
    plot = px.histogram(x=data['model_year'], title="Histogram for model_year", labels={'x': 'Model Year', 'y': 'Number of ads'}, nbins=50)
    st.plotly_chart(plot, use_container_width=True)

    # Histogram for `price`
    plot = px.histogram(x=data['price'], title="Histogram for price", labels={'x': 'Price', 'y': 'Number of ads'}, nbins=50)
    st.plotly_chart(plot, use_container_width=True)

# Display scatter plots if option is checked
if show_scatter:
    st.header('Vehicle Ads - Scatter Plots for Model Year and Odometer')

    # Scatterplot for model_year and odometer
    column_list = ['model_year', 'odometer']

    for col in column_list:
        plot = px.scatter(data, x='price', y=col, title=f'Scatter Plot for Price vs {col}',
                        labels={'price': 'Price', col: col},
                        opacity=0.1)
        st.plotly_chart(plot, use_container_width=True)