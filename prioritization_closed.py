import pandas as pd
import numpy as np

# Read the CSV file into a DataFrame
file_path = 'closed_cases.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Define the importance order of case types
case_type_order = {
    'Terrorism': 1,
    'Counterintelligence': 2,
    'Cyber Crime': 3,
    'Public Corruption': 4,
    'Civil Rights': 5,
    'Organized Crime': 6,
    'White-Collar Crime': 7,
    'Violent Crimes': 8,
    'Major Thefts': 9,
    'Intellectual Property Violations': 10,
    'Environmental Law Violations': 11,
    'Employment Law Disputes': 12,
    'Immigration Law Cases': 13,
    'Securities Fraud': 14,
    'Drug Trafficking': 15
}

print(df.columns)

# Map the case types to their corresponding importance order
df['Case Type Priority'] = df['Case Type'].map(case_type_order)

# Convert date columns to datetime format
date_columns = ['Filing Date', 'Hearing 1 date', 'Hearing 2 date', 'Hearing 3 date']
df[date_columns] = df[date_columns].apply(pd.to_datetime, format='%d.%m.%y')

# Calculate age of case based on filing date
df['Case Age'] = (pd.to_datetime('now') - df['Filing Date']).dt.days

# Calculate number of scheduled hearings for each case
df['Scheduled Hearings'] = df[date_columns[1:]].count(axis=1)

# Normalize values for Case Age and Scheduled Hearings for prioritization
df['Case Age'] = (df['Case Age'] - df['Case Age'].min()) / (df['Case Age'].max() - df['Case Age'].min())
df['Scheduled Hearings'] = (df['Scheduled Hearings'] - df['Scheduled Hearings'].min()) / (df['Scheduled Hearings'].max() - df['Scheduled Hearings'].min())

# Calculate overall priority score considering all criteria
df['Overall Priority'] = df['Case Type Priority'] + df['Case Age'] + df['Scheduled Hearings'].fillna(0)

# Sort the DataFrame based on the overall priority score
df_sorted = df.sort_values(by='Overall Priority', ascending=True)

# Display prioritized cases or save to a new CSV file
print(df_sorted[['Case ID', 'Case Type', 'Filing Date', 'Case Age', 'Scheduled Hearings', 'Overall Priority']])

# To save the prioritized data to a new CSV file
df_sorted.to_csv('prioritized_closed_cases.csv', index=False)
