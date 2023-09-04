import pandas as pd
import scipy.stats
import streamlit as st
import time
from matplotlib import pyplot as plt
import plotly.express as px

# Load the data file into a DataFrame
data = pd.read_csv('vehicles_us.csv', sep=',')

# Cylinders - Replace NaN values with the mode based on 'model_year' and 'model'
# Function to get mode of cylinder values
def get_mode(cylinder_values):
    mode_values = cylinder_values.mode()
    if len(mode_values) > 1:
        return mode_values.min()
    else:
        return mode_values[0]

# Build new dataframe using groupby and rename columns
data_model = data.dropna(subset=['cylinders']).groupby(['model_year', 'model'])['cylinders'].agg(get_mode).reset_index(name='cylinders_mode')

# Ensure column doesn't exist in data
if 'cylinders_mode' in data.columns:
    data = data.drop('cylinders_mode', axis=1)

# Merge both dataframes
data = data.merge(data_model, on=['model_year', 'model'], how='left')

# Replace null values with mode
data['cylinders'].fillna(value=data['cylinders_mode'], inplace=True)

# Delete newly added column
data.drop(columns=['cylinders_mode'], inplace=True)

# Cylinders - Replace remaining NaN values with the mode based on 'model'
# Build new dataframe using groupby and rename columns
data_model = data.groupby(['model'])['cylinders'].agg(pd.Series.mode).reset_index(name='cylinders_mode')

# Ensure column doesn't exist in data_filtered
if 'cylinders_mode' in data.columns:
    data = data.drop('cylinders_mode', axis=1)

# Merge both dataframes
data = data.merge(data_model, on=['model'], how='left')

# Replace null values
data['cylinders'].fillna(value=data['cylinders_mode'], inplace=True)

# Delete newly added column
data.drop(columns=['cylinders_mode'], inplace=True)

# Model Year - Replace NaN values with the median based on 'model', 'condition', 'odometer_rounded'
# Create a field to categorize the `odometer` values
data['odometer_rounded'] = (data['odometer'] // 10000)*10000

# Create a new DataFrame to keep the median from each combination
data_model_median = data.groupby(['model', 'condition', 'odometer_rounded'])['model_year'].median().dropna().astype(int)

# Merge with the original DataFrame
data = data.merge(data_model_median, on=['model', 'condition', 'odometer_rounded'], how='left', suffixes=(None, '_2'))

# Fill NaN values with the merged column
data['model_year'].fillna(value=data['model_year_2'], inplace=True)

# Remove the new column
data.drop(columns=['model_year_2'], inplace=True)

# Odometer - Replace NaN values with the median based on 'model_year', 'model', 'condition'
# Create a new DataFrame to keep the median from each combination
data_model_median = data.groupby(['model_year', 'model', 'condition'])['odometer'].median()

# Merge with the original DataFrame
data = data.merge(data_model_median, on=['model_year', 'model', 'condition'], how='left', suffixes=(None, '_2'))

# Fill NaN values with the merged column
data['odometer'].fillna(value=data['odometer_2'], inplace=True)

# Remove the new column
data.drop(columns=['odometer_2'], inplace=True)

# Convert `model_year` from a float to int
data['model_year'] = data['model_year'].dropna().astype(int)

# Convert `cylinders` from a float to int
data['cylinders'] = data['cylinders'].dropna().astype(int)

# Store data without outliers in a separate DataFrame
data_filtered = data[(data['price'].between(1000, 50000)) & (data['model_year'] > 1990) & (data['odometer'] < 400000) &
                     (((data['condition'] == 'new') & (data['odometer'] > 5)) | 
                      ((data['condition'] != 'new') & (data['odometer'] > 100)))].copy()

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
    plot = px.histogram(x=data_filtered['model_year'], title="Histogram for model_year", labels={'x': 'Model Year', 'y': 'Number of ads'}, nbins=50)
    st.plotly_chart(plot, use_container_width=True)

    # Histogram for `price`
    plot = px.histogram(x=data_filtered['price'], title="Histogram for price", labels={'x': 'Price', 'y': 'Number of ads'}, nbins=50)
    st.plotly_chart(plot, use_container_width=True)

# Display scatter plots if option is checked
if show_scatter:
    st.header('Vehicle Ads - Scatter Plots for Model Year, Odometer, Cylinders')

    # Scatterplot for model_year and odometer
    column_list = ['model_year', 'odometer', 'cylinders']

    for col in column_list:
        plot = px.scatter(data_filtered, x='price', y=col, title=f'Scatter Plot for Price vs {col}',
                        labels={'price': 'Price', col: col},
                        opacity=0.1)
        st.plotly_chart(plot, use_container_width=True)