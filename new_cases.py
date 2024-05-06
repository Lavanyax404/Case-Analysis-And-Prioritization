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
    # Format date to dd.mm.yy
    filing_date_formatted = filing_date.strftime("%d.%m.%y") if filing_date else None
    hearing1_date_formatted = hearing_1_date.strftime("%d.%m.%y") if hearing_1_date else None
    hearing2_date_formatted = hearing_2_date.strftime("%d.%m.%y") if hearing_2_date else None
    hearing3_date_formatted = hearing_3_date.strftime("%d.%m.%y") if hearing_3_date else None
    
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

st.markdown('<p style="text-align: center; font-size: 48px;">🏛️</p>', unsafe_allow_html=True)
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
