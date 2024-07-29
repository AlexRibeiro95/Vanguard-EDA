import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend import load_data, get_summary, plot_high_value_customers, plot_primary_customers, plot_design_effectiveness, plot_time_to_completion

# Load data
data = load_data()

# Streamlit app layout
st.title('Vanguard Investment Project Dashboard')

# Display summary statistics
st.header('Summary Statistics')
summary = get_summary(data)
st.write(summary)

# Display high value customers
st.header('High Value Customers')
plt = plot_high_value_customers(data)
st.pyplot(plt)

# Display primary customers
st.header('Primary Customers')
plt = plot_primary_customers(data)
st.pyplot(plt)

# Display design effectiveness
st.header('Design Effectiveness: Completion Rates')
plt = plot_design_effectiveness(data)
st.pyplot(plt)

# Display time to completion
st.header('Time to Completion')
plt = plot_time_to_completion(data)
st.pyplot(plt)

# Optionally add more sections and interactive elements