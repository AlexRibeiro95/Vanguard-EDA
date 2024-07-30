import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Function to load the data
def load_data():
    df_merged = pd.read_csv('https://raw.githubusercontent.com/h4Sh1G/Vanguard-EDA/main/data/clean/df_merged_final.csv')
    df_cleaned = pd.read_csv('https://raw.githubusercontent.com/h4Sh1G/Vanguard-EDA/main/data/clean/df_cleaned.csv')
    return df_merged, df_cleaned

# Function to get upper quartiles
def get_upper_quartiles(data, columns):
    upper_quartiles = {}
    for col in columns:
        upper_quartiles[col] = (data[col].quantile(0.75), data[col].max())
    return upper_quartiles

# Function to plot high value clients
def plot_high_value_clients(data):
    fig_gender = px.bar(data['gender'].value_counts(), title="Gender Distribution of High Value Clients")
    fig_tenure = px.histogram(data, x='clnt_tenure_yr', title="Tenure Distribution of High Value Clients")
    fig_age = px.histogram(data, x='clnt_age', title="Age Distribution of High Value Clients")
    return fig_gender, fig_tenure, fig_age

# Function to plot primary clients
def plot_primary_clients(data):
    fig_gender = px.bar(data['gender'].value_counts(), title="Gender Distribution of Primary Clients")
    fig_tenure = px.histogram(data, x='clnt_tenure_yr', title="Tenure Distribution of Primary Clients")
    fig_age = px.histogram(data, x='clnt_age', title="Age Distribution of Primary Clients")
    return fig_gender, fig_tenure, fig_age

# Function to plot design effectiveness
def plot_design_effectiveness(data):
    data['completed'] = data['process_step'] == 'confirm'
    completion_rate_control = data[(data['variation'] == 'Control') & (data['completed'])].shape[0] / data[data['variation'] == 'Control']['visit_id'].nunique()
    completion_rate_test = data[(data['variation'] == 'Test') & (data['completed'])].shape[0] / data[data['variation'] == 'Test']['visit_id'].nunique()
    fig = px.bar(x=['Control', 'Test'], y=[completion_rate_control, completion_rate_test], labels={'x': 'Group', 'y': 'Completion Rate'}, title="Completion Rate by Group")
    return fig

# Function to plot time to completion
def plot_time_to_completion(data):
    data['date_time'] = pd.to_datetime(data['date_time'])
    data['completion_time'] = data.groupby('visit_id')['date_time'].transform(lambda x: x.max() - x.min())
    completion_times = data[data['process_step'] == 'confirm'].groupby('variation')['completion_time'].mean().dt.total_seconds() / 3600
    fig = px.bar(completion_times, labels={'index': 'Group', 'value': 'Average Completion Time (Hours)'}, title="Average Completion Time by Group")
    return fig

# Function to plot power analysis
def plot_power_analysis(data):
    import statsmodels.stats.power as smp
    effect_size = 0.0632  # Example effect size
    alpha = 0.05
    sample_sizes = range(1000, 20000, 500)
    powers = [smp.tt_ind_solve_power(effect_size=effect_size, nobs1=n, alpha=alpha, power=None, ratio=1.0) for n in sample_sizes]
    fig = px.line(x=sample_sizes, y=powers, labels={'x': 'Sample Size per Group', 'y': 'Power'}, title='Power Curve')
    fig.add_hline(y=0.8, line_dash="dash", line_color="red")
    return fig

def plot_normalization_graph_interactive(data):
    data['date_time'] = pd.to_datetime(data['date_time'])
    data['completed'] = data['process_step'] == 'confirm'
    
    # Group by date, variation, and visit_id, then take the maximum 'completed' value per visit
    grouped = data.groupby([data['date_time'].dt.date, 'variation', 'visit_id'])['completed'].max().reset_index()

    # Pivot the data to get cumulative completion rates
    pivoted = grouped.pivot_table(index='date_time', columns='variation', values='completed', aggfunc='mean').fillna(0)

    # Calculate cumulative mean completion rates
    cumulative_data = pivoted.cumsum() / np.arange(1, len(pivoted) + 1).reshape(-1, 1)
    cumulative_data = cumulative_data.reset_index()

    # Plot cumulative completion rates using Plotly Express
    fig = px.line(cumulative_data, x='date_time', y=['Control', 'Test'], labels={'value': 'Cumulative Completion Rate', 'date_time': 'Date'}, title='Cumulative Completion Rates Over Time')
    fig.update_layout(yaxis_title='Cumulative Completion Rate', xaxis_title='Date', legend_title_text='Group')

    return fig