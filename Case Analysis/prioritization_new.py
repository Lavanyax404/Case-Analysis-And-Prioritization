import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime
import matplotlib.pyplot as plt
import seaborn as sns


# Streamlit app
st.set_page_config(page_title="🏛 Case Analytics & Prioritization")
st.markdown('<p style="text-align: center; font-size: 48px;">🏛️</p>', unsafe_allow_html=True)
st.title('Case Analytics')
df=pd.read_csv('pending_cases.csv')
# Adding Visualizations

# Case Type Distribution
st.subheader('Case Type Distribution')
case_type_counts = df['Case Type'].value_counts()
fig_case_type = plt.figure(figsize=(8, 6))
with sns.color_palette(['darkblue']):
    sns.barplot(y=case_type_counts.index, x=case_type_counts.values, orient='h')

plt.xlabel('Count')
plt.ylabel('Case Type')
plt.xticks(rotation=45)
st.pyplot(fig_case_type)

df['Number of Hearings'] = df[['Hearing 1 date', 'Hearing 2 date', 'Hearing 3 date']].count(axis=1)

# Group cases by the number of hearings and count the occurrences
cases_by_hearings = df['Number of Hearings'].value_counts().sort_index()

# Create a bar plot for number of hearings vs number of cases
st.subheader('Number of Hearings vs Number of Cases')
fig_hearings_vs_cases = plt.figure(figsize=(8, 6))
sns.barplot(x=cases_by_hearings.index, y=cases_by_hearings.values)
plt.xlabel('Number of Hearings')
plt.ylabel('Number of Cases')
st.pyplot(fig_hearings_vs_cases)

# Calculate the count of cases for each judge
cases_per_judge = df['Assigned Judge'].value_counts().sort_index()

# Get all unique judges from the 'Assigned Judge' field
all_judges = df['Assigned Judge'].unique()

# Display a multiselect widget to select judges
selected_judges = st.multiselect('Select Judges', all_judges)

if selected_judges:
    # Filter the DataFrame for selected judges
    filtered_cases_per_judge = df[df['Assigned Judge'].isin(selected_judges)]['Assigned Judge'].value_counts().sort_index()

    # Create a line chart for number of cases per selected judge
    st.subheader('Number of Cases for Selected Judges')
    fig_filtered_cases_per_judge = plt.figure(figsize=(10, 6))

    # Temporarily set the color to green for this plot
    with sns.color_palette(['green']):
        sns.lineplot(x=filtered_cases_per_judge.index, y=filtered_cases_per_judge.values, marker='o', orient='x')
    plt.xlabel('Assigned Judge')
    plt.ylabel('Number of Cases')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig_filtered_cases_per_judge)


# Function to prioritize DataFrame based on criteria
def prioritize_dataframe(dataframe):
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

    # Define date columns
    date_columns = ['Filing Date', 'Hearing 1 date', 'Hearing 2 date', 'Hearing 3 date']

    # Convert date columns to datetime format and format to '%d.%m.%y'
    pending_cases[date_columns] = pending_cases[date_columns].apply(pd.to_datetime, format='%d.%m.%y')

    # Calculate the age of the case based on filing date (with higher priority for older cases)
    pending_cases['Filing Date'] = pd.to_datetime(pending_cases['Filing Date'], format='%d.%m.%y')
    pending_cases['Case Age'] = (pd.to_datetime('now').normalize() - pending_cases['Filing Date'].dt.normalize()).dt.days
    pending_cases['Case Age'] = pending_cases['Case Age'].max() - pending_cases['Case Age']  # Higher age, higher priority

    # Format the date columns to '%d.%m.%y'
    for col in date_columns:
        pending_cases[col] = pending_cases[col].dt.strftime('%d.%m.%y')


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

    pending_cases_sorted.reset_index(drop=True, inplace=True)
    pending_cases_sorted.index += 1  # Adding 1 to start from 1

    st.title('Prioritized Pending Cases')
    st.write(pending_cases_sorted[['Case ID', 'Case Type', 'Filing Date', 'Case Title']])

# Streamlit app

import streamlit as st
import pandas as pd


# Function to update CSV file with DataFrame
def update_csv(dataframe, filename):
    dataframe.to_csv(filename, index=False)

# Load existing CSV file or create a new one if it doesn't exist
filename = 'pending_cases.csv'
try:
    df = pd.read_csv(filename)
except FileNotFoundError:
    df = pd.DataFrame({
        'Case ID': [],
        'Case Type': [],
        'Parties Involved': [],
        'Case Title': [],
        'Filing Date': [],
        'Case Status': [],
        'Case Location': [],
        'Hearing 1 date': [],
        'Hearing 2 date': [],
        'Hearing 3 date': [],
        'Assigned Judge': []
    })

# Function to generate auto-incremented Case ID
def generate_case_id(dataframe):
    if dataframe.empty:
        return '3001'
    else:
        max_case_id = dataframe['Case ID'].max()
        return str(max_case_id + 1)

# Function to update DataFrame based on user input
def update_dataframe(case_type, parties_involved, filing_date, case_location, hearing_1_date, hearing_2_date, hearing_3_date, assigned_judge):
    global df  # Access the global variable df inside the function
    case_id = generate_case_id(df)
    def format_date(date):
        return date.strftime("%d.%m.%y") if date else None
    
    filing_date_formatted = format_date(filing_date)
    hearing1_date_formatted = format_date(hearing_1_date)
    hearing2_date_formatted = format_date(hearing_2_date)
    hearing3_date_formatted = format_date(hearing_3_date)
    
    new_entry = {
        'Case ID': case_id,
        'Case Type': case_type,
        'Parties Involved': parties_involved,
        'Case Title': f'{case_type} - {parties_involved}',
        'Filing Date': filing_date_formatted,
        'Case Status': 'Pending',  # Set default value for Case Status as "Pending"
        'Case Location': case_location,
        'Hearing 1 date': hearing1_date_formatted,
        'Hearing 2 date': hearing2_date_formatted,
        'Hearing 3 date': hearing3_date_formatted,
        'Assigned Judge': assigned_judge
    }
    # Convert new entry to DataFrame and concatenate it with the existing DataFrame
    new_df_entry = pd.DataFrame([new_entry])
    df = pd.concat([df, new_df_entry], ignore_index=True)
    
    return df

# Streamlit app

st.title('New Case Entry')

# Form to take user input
case_type_options = sorted(df['Case Type'].unique())
assigned_judge_options = sorted(df['Assigned Judge'].unique())
case_location_options = sorted(df['Case Location'].unique())

case_type = st.selectbox('Case Type', case_type_options)
parties_involved = st.text_input('Parties Involved')
filing_date = st.date_input('Filing Date')
case_location = st.selectbox('Case Location', case_location_options)
hearing_1_date = st.date_input('Hearing 1 date', None)
hearing_2_date = st.date_input('Hearing 2 date', None)
hearing_3_date = st.date_input('Hearing 3 date', None)
assigned_judge = st.selectbox('Assigned Judge', assigned_judge_options)

# Button to trigger update
if st.button('Add Case'):
    if case_type and parties_involved and filing_date and case_location and (
            hearing_1_date is not None or hearing_2_date is not None or hearing_3_date is not None):
        df = update_dataframe(case_type, parties_involved, filing_date, case_location,
                              hearing_1_date, hearing_2_date, hearing_3_date, assigned_judge)
        update_csv(df, filename)  # Update CSV file with new data
        st.success('Case added successfully!')
    else:
        st.warning('Please fill in required fields.')

# Display updated DataFrame
st.write('Pending Cases:', df)


# Display prioritized DataFrame
if st.button('Show Prioritized Cases'):
    prioritized_df = prioritize_dataframe(df)  # Prioritize the DataFrame
    
