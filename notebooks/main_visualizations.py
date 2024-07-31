# Import necessary libraries
import pandas as pd

# Step 1: Load Data
def load_data():
    df_cleaned = pd.read_csv('/Users/alexandreribeiro/Desktop/Ironhacks Booty/5th week/Project/Datasets/df_cleaned.csv')
    return df_cleaned

# Step 2: Divide Data into Control and Test Samples
def divide_data(df_cleaned, sample_size=100000):
    df_control = df_cleaned[df_cleaned['variation'] == 'Control'].sample(n=sample_size, random_state=42)
    df_test = df_cleaned[df_cleaned['variation'] == 'Test'].sample(n=sample_size, random_state=42)
    return df_control, df_test

# Step 3: Export to CSV
def export_to_csv(df_control, df_test):
    df_control.to_csv('control_group_data.csv', index=False)
    df_test.to_csv('test_group_data.csv', index=False)

def main():
    # Load the data
    df_cleaned = load_data()
    
    # Divide the data into Control and Test samples
    df_control, df_test = divide_data(df_cleaned)
    
    # Export the divided data to CSV files
    export_to_csv(df_control, df_test)

if __name__ == "__main__":
    main()