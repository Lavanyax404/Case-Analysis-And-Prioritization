import pandas as pd
from faker import Faker
import random
from datetime import timedelta

fake = Faker()

# Function to generate a dataset for pending cases
def generate_pending_cases(num_cases):
    case_types = [
        'Terrorism', 'Counterintelligence', 'Cyber Crime', 'Public Corruption',
        'Civil Rights', 'Organized Crime', 'White-Collar Crime', 'Violent Crimes',
        'Major Thefts', 'Intellectual Property Violations', 'Environmental Law Violations',
        'Employment Law Disputes', 'Immigration Law Cases', 'Securities Fraud', 'Drug Trafficking'
    ]

    location = [
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio',
        'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'San Francisco', 'Indianapolis',
        'Columbus', 'Fort Worth', 'Charlotte', 'Seattle', 'Denver', 'Washington', 'Boston', 'Detroit',
        'Nashville', 'Memphis', 'Portland', 'Oklahoma City', 'Las Vegas', 'Louisville', 'Baltimore', 'Milwaukee'
    ]

    pending_cases = []
    judges = [fake.name() for _ in range(250)]

    for i in range(num_cases):
        case_id = i + 1
        case_type = random.choice(case_types)
        offender_name = fake.first_name_male() if random.choice([True, False]) else fake.first_name_female()
        case_title = f"{case_type} Case - {offender_name}"
        filing_date = fake.date_between(start_date='-2y', end_date='today')
        case_status = 'Pending'
        case_location = random.choice(location)
        hearing_1_date = fake.date_between(start_date=filing_date, end_date='+1y')
    
        # Ensure hearing dates are within a feasible range
        max_date = hearing_1_date + timedelta(days=365)  # Maximum 1 year from hearing 1 date
        hearing_2_date = fake.date_between(start_date=hearing_1_date, end_date=max_date) if random.random() > 0.3 else None
        if hearing_2_date:
            max_date = hearing_2_date + timedelta(days=182)  # Maximum 6 months from hearing 2 date
            hearing_3_date = fake.date_between(start_date=hearing_2_date, end_date=max_date) if random.random() > 0.3 else None
        else:
            hearing_3_date = None
        assigned_judge = random.choice(judges)

        pending_cases.append([case_id, case_type, offender_name, case_title, filing_date, case_status, case_location,hearing_1_date,hearing_2_date,hearing_3_date, assigned_judge])

    columns = ['Case ID', 'Case Type', 'Parties Involved', 'Case Title', 'Filing Date', 'Case Status', 'Case Location', 'Hearing 1 date' , 'Hearing 2 date' ,'Hearing 3 date', 'Assigned Judge']
    pending_df = pd.DataFrame(pending_cases, columns=columns)
    return pending_df

# Function to generate a dataset for closed cases
def generate_closed_cases(num_cases):
    case_types = [
        'Terrorism', 'Counterintelligence', 'Cyber Crime', 'Public Corruption',
        'Civil Rights', 'Organized Crime', 'White-Collar Crime', 'Violent Crimes',
        'Major Thefts', 'Intellectual Property Violations', 'Environmental Law Violations',
        'Employment Law Disputes', 'Immigration Law Cases', 'Securities Fraud', 'Drug Trafficking'
    ]

    location = [
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio',
        'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'San Francisco', 'Indianapolis',
        'Columbus', 'Fort Worth', 'Charlotte', 'Seattle', 'Denver', 'Washington', 'Boston', 'Detroit',
        'Nashville', 'Memphis', 'Portland', 'Oklahoma City', 'Las Vegas', 'Louisville', 'Baltimore', 'Milwaukee'
    ]

    closed_cases = []
    judges = [fake.name() for _ in range(250)]

    for i in range(num_cases):
        case_id = i + 1
        case_type = random.choice(case_types)
        offender_name = fake.first_name_male() if random.choice([True, False]) else fake.first_name_female()
        case_title = f"{case_type} Case - {offender_name}"
        filing_date = fake.date_between(start_date='-2y', end_date='today')
        case_status = 'Closed'
        case_location = random.choice(location)
        hearing_1_date = fake.date_between(start_date=filing_date, end_date='+1y')
    
        # Ensure hearing dates are within a feasible range
        max_date = hearing_1_date + timedelta(days=365)  # Maximum 1 year from hearing 1 date
        hearing_2_date = fake.date_between(start_date=hearing_1_date, end_date=max_date) if random.random() > 0.3 else None
        if hearing_2_date:
            max_date = hearing_2_date + timedelta(days=182)  # Maximum 6 months from hearing 2 date
            hearing_3_date = fake.date_between(start_date=hearing_2_date, end_date=max_date) if random.random() > 0.3 else None
        else:
            hearing_3_date = None
            
        assigned_judge = random.choice(judges)

        closed_cases.append([case_id, case_type, offender_name, case_title, filing_date, case_status, case_location,hearing_1_date,hearing_2_date,hearing_3_date, assigned_judge])

    columns = ['Case ID', 'Case Type', 'Parties Involved', 'Case Title', 'Filing Date', 'Case Status', 'Case Location', 'Hearing 1 date' , 'Hearing 2 date' ,'Hearing 3 date', 'Assigned Judge']
    closed_df = pd.DataFrame(closed_cases, columns=columns)
    return closed_df

# Generating datasets
num_pending_cases = 3000  # Adjust as needed
num_closed_cases = 2000  # Adjust as needed

pending_cases_df = generate_pending_cases(num_pending_cases)
closed_cases_df = generate_closed_cases(num_closed_cases)

# Save datasets to CSV files
pending_cases_df.to_csv('pending_cases.csv', index=False)
closed_cases_df.to_csv('closed_cases.csv', index=False)
