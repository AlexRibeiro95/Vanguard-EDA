import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    # Load all datasets using raw GitHub URLs
    df_demo = pd.read_csv('https://raw.githubusercontent.com/h4Sh1G/Vanguard-EDA/main/data/raw/df_final_demo.csv')
    df_experiment = pd.read_csv('https://raw.githubusercontent.com/h4Sh1G/Vanguard-EDA/main/data/raw/df_final_experiment_clients.csv')
    df_web_data_1 = pd.read_csv('https://raw.githubusercontent.com/h4Sh1G/Vanguard-EDA/main/data/raw/df_final_web_data_pt_1.csv')
    df_web_data_2 = pd.read_csv('https://raw.githubusercontent.com/h4Sh1G/Vanguard-EDA/main/data/raw/df_final_web_data_pt_2.csv')
    
    # Combine web data
    df_web_data = pd.concat([df_web_data_1, df_web_data_2])
    
    # Merge datasets
    df_merged = df_demo.merge(df_experiment, on='client_id', how='inner').merge(df_web_data, on='client_id', how='inner')
    
    # Print merged DataFrame columns for debugging
    print("df_merged columns:", df_merged.columns)
    
    return df_merged

def get_summary(data):
    summary = pd.DataFrame({
        'Total Clients': [data['client_id'].nunique()],
        'Average Age': [data['clnt_age'].mean()],
        'Average Balance': [data['bal'].mean()],
        'Total Transactions': [data['visit_id'].nunique()]
    })
    return summary

def plot_high_value_customers(data):
    high_value_customers = data[data['bal'] > data['bal'].quantile(0.9)]
    plt.figure(figsize=(10, 5))
    plt.hist(high_value_customers['bal'], bins=50)
    plt.title('High Value Customers Balance Distribution')
    plt.xlabel('Balance')
    plt.ylabel('Frequency')
    plt.tight_layout()
    return plt

def plot_primary_customers(data):
    primary_customers = data[(data['clnt_age'] > data['clnt_age'].median()) & (data['clnt_tenure_yr'] > data['clnt_tenure_yr'].median())]
    plt.figure(figsize=(10, 5))
    plt.scatter(primary_customers['clnt_tenure_yr'], primary_customers['clnt_age'], alpha=0.5)
    plt.title('Primary Customers: Age vs Tenure')
    plt.xlabel('Tenure (Years)')
    plt.ylabel('Age')
    plt.tight_layout()
    return plt

def plot_design_effectiveness(data):
    data['completed'] = data['process_step'] == 'confirm'
    completion_rate_control = data[(data['Variation'] == 'Control') & (data['completed'])].shape[0] / data[data['Variation'] == 'Control']['visit_id'].nunique()
    completion_rate_test = data[(data['Variation'] == 'Test') & (data['completed'])].shape[0] / data[data['Variation'] == 'Test']['visit_id'].nunique()

    labels = ['Control', 'Test']
    sizes = [completion_rate_control, completion_rate_test]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title('Completion Rates: Control vs Test')
    plt.tight_layout()
    return plt

def plot_time_to_completion(data):
    data['date_time'] = pd.to_datetime(data['date_time'])
    # Calculate the minimum and maximum times for each client and variation
    min_times = data.groupby(['client_id', 'Variation'])['date_time'].min()
    max_times = data.groupby(['client_id', 'Variation'])['date_time'].max()
    # Calculate completion times
    completion_times = (max_times - min_times).dt.total_seconds() / 3600  # Convert to hours
    completion_times = completion_times.reset_index(name='completion_time_hours')
    # Merge completion times back to the original data
    data = data.merge(completion_times, on=['client_id', 'Variation'], how='left')
    # Plot
    plt.figure(figsize=(10, 5))
    data.boxplot(column='completion_time_hours', by='Variation')
    plt.title('Time to Completion by Variation')
    plt.xlabel('Variation')
    plt.ylabel('Time (Hours)')
    plt.suptitle('')  # Suppress the default title
    plt.tight_layout()
    return plt