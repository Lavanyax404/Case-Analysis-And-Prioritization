import pandas as pd
from sklearn.linear_model import LinearRegression
import streamlit as st

# Read the CSV files into DataFrames
prioritized_closed_cases = pd.read_csv('prioritized_closed_cases.csv')
pending_cases = pd.read_csv('pending_cases.csv')

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

# Map the case types to their corresponding importance order
pending_cases['Case Type Priority'] = pending_cases['Case Type'].map(case_type_order)

# Convert date columns to datetime format and format to '%d.%m.%y'
date_columns = ['Filing Date', 'Hearing 1 date', 'Hearing 2 date', 'Hearing 3 date']
pending_cases[date_columns] = pending_cases[date_columns].apply(pd.to_datetime, format='%d.%m.%y')

# Format date columns to '%d.%m.%y'
for col in date_columns:
    pending_cases[col] = pending_cases[col].dt.strftime('%d.%m.%y')
# Calculate the age of the case based on filing date (with higher priority for older cases)
pending_cases['Filing Date'] = pd.to_datetime(pending_cases['Filing Date'], format='%d.%m.%y')  # Ensure datetime format
pending_cases['Case Age'] = (pd.to_datetime('now').normalize() - pending_cases['Filing Date'].dt.normalize()).dt.days
pending_cases['Case Age'] = pending_cases['Case Age'].max() - pending_cases['Case Age']  # Higher age, higher priority

# Calculate number of scheduled hearings for each pending case
pending_cases['Scheduled Hearings'] = pending_cases[date_columns[1:]].count(axis=1)

# Normalize values for Case Age and Scheduled Hearings for prioritization
pending_cases['Scheduled Hearings'] = (pending_cases['Scheduled Hearings'] - pending_cases['Scheduled Hearings'].min()) / (pending_cases['Scheduled Hearings'].max() - pending_cases['Scheduled Hearings'].min())

# Calculate an overall priority score considering all criteria for pending cases
pending_cases['Overall Priority'] = pending_cases['Case Type Priority'] + pending_cases['Case Age'] + pending_cases['Scheduled Hearings'].fillna(0)

# Define features and target for model training
features = ['Case Type Priority', 'Case Age', 'Scheduled Hearings']
X_train = prioritized_closed_cases[features]
y_train = prioritized_closed_cases['Overall Priority']

# Train a Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Use the trained model to predict priorities for pending cases
X_pending = pending_cases[features]
pending_cases['Predicted Priority'] = model.predict(X_pending)

# Sort pending cases based on the predicted priority score
pending_cases_sorted = pending_cases.sort_values(by='Predicted Priority', ascending=True)

# Display or save the prioritized pending cases
print(pending_cases_sorted[['Case ID', 'Case Type', 'Filing Date', 'Case Title']])

# To save the prioritized pending cases to a new CSV file
pending_cases_sorted.to_csv('prioritized_pending_cases.csv', index=False)
st.title('Prioritized Pending Cases')
st.write(pending_cases_sorted[['Case ID', 'Case Type', 'Filing Date', 'Case Title']])


