import io
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from backend import (
    load_data, get_upper_quartiles, plot_high_value_clients,
    plot_primary_clients, plot_design_effectiveness, plot_time_to_completion,
    plot_power_analysis, plot_normalization_graph_interactive
)

st.set_page_config(layout="wide", page_title="Vanguard Project - Clients Analysis", page_icon="🏨")

# Function to download data as CSV
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

# Load data
df_merged, df_cleaned = load_data()

# Calculate upper quartile intervals
upper_quartiles_merged = get_upper_quartiles(df_merged, ['balance', 'clnt_tenure_yr'])
upper_quartiles_cleaned = get_upper_quartiles(df_cleaned, ['balance', 'clnt_tenure_yr'])

# Sidebar filters
st.sidebar.title("Filters")
dataset_choice = st.sidebar.selectbox("Select Dataset", ["High Value Clients", "Primary Clients"])
balance_filter = st.sidebar.slider('Select Balance Range', min_value=int(df_merged['balance'].min()), max_value=int(df_merged['balance'].max()), value=(int(df_merged['balance'].min()), int(df_merged['balance'].max())))
tenure_filter = st.sidebar.slider('Select Tenure Range', min_value=int(df_merged['clnt_tenure_yr'].min()), max_value=int(df_merged['clnt_tenure_yr'].max()), value=(int(df_merged['clnt_tenure_yr'].min()), int(df_merged['clnt_tenure_yr'].max())))
age_filter = st.sidebar.slider('Select Age Range', min_value=int(df_merged['clnt_age'].min()), max_value=int(df_merged['clnt_age'].max()), value=(int(df_merged['clnt_age'].min()), int(df_merged['clnt_age'].max())))
gender_filter = st.sidebar.multiselect('Select Gender', df_merged['gender'].unique(), df_merged['gender'].unique())
variation_filter = st.sidebar.multiselect('Group', df_merged['variation'].unique(), df_merged['variation'].unique())

# Filtered data
if dataset_choice == "High Value Clients":
    filtered_data = df_merged[(df_merged['balance'].between(*balance_filter)) &
                              (df_merged['clnt_tenure_yr'].between(*tenure_filter)) &
                              (df_merged['clnt_age'].between(*age_filter)) &
                              (df_merged['gender'].isin(gender_filter)) &
                              (df_merged['variation'].isin(variation_filter))]
else:
    filtered_data = df_cleaned[(df_cleaned['balance'].between(*balance_filter)) &
                               (df_cleaned['clnt_tenure_yr'].between(*tenure_filter)) &
                               (df_cleaned['clnt_age'].between(*age_filter)) &
                               (df_cleaned['gender'].isin(gender_filter)) &
                               (df_cleaned['variation'].isin(variation_filter))]
    
# Display filtered data table
st.title("Data Overview")
st.write(f"### {dataset_choice}")
st.write(filtered_data)

# Add download button for filtered data
csv_filtered = convert_df_to_csv(filtered_data)
st.download_button(
    label="Download filtered data as CSV",
    data=csv_filtered,
    file_name='filtered_data.csv',
    mime='text/csv',
)

# Display upper quartile intervals
st.write("### Upper Quartile Intervals")
st.write("**Merged Dataset (High Value Clients)**")
st.write(f"Balance: {upper_quartiles_merged['balance'][0]:.2f} - {upper_quartiles_merged['balance'][1]:.2f}")
st.write(f"Tenure: {upper_quartiles_merged['clnt_tenure_yr'][0]:.2f} - {upper_quartiles_merged['clnt_tenure_yr'][1]:.2f}")
st.write("**Cleaned Dataset (Primary Clients)**")
st.write(f"Balance: {upper_quartiles_cleaned['balance'][0]:.2f} - {upper_quartiles_cleaned['balance'][1]:.2f}")
st.write(f"Tenure: {upper_quartiles_cleaned['clnt_tenure_yr'][0]:.2f} - {upper_quartiles_cleaned['clnt_tenure_yr'][1]:.2f}")

# Plot visualizations based on dataset choice
if dataset_choice == "High Value Clients":
    st.title("High Value Clients Analysis")
    fig_gender, fig_tenure, fig_age = plot_high_value_clients(filtered_data)
    st.plotly_chart(fig_gender)
    st.plotly_chart(fig_tenure)
    st.plotly_chart(fig_age)
else:
    st.title("Primary Clients Analysis")
    fig_gender, fig_tenure, fig_age = plot_primary_clients(filtered_data)
    st.plotly_chart(fig_gender)
    st.plotly_chart(fig_tenure)
    st.plotly_chart(fig_age)

# Plot design effectiveness
st.title("Design Effectiveness")
fig_design_effectiveness = plot_design_effectiveness(df_merged)
st.plotly_chart(fig_design_effectiveness)

# Plot time to completion
st.title("Time to Completion")
fig_time_to_completion = plot_time_to_completion(df_merged)
st.plotly_chart(fig_time_to_completion)

# Plot power analysis
st.title("Power Analysis")
fig_power_analysis = plot_power_analysis(df_merged)
st.plotly_chart(fig_power_analysis)

# Plot normalization graph
st.title("Normalization Graph")
fig_normalization_graph = plot_normalization_graph_interactive(df_merged)
st.plotly_chart(fig_normalization_graph)

