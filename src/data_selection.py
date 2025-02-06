# Selects relevant dataframes for calculations

import pandas

REQUIRED_SECTIONS = [
    'Realized & Unrealized Performance Summary', 
    'Trade Summary by Symbol', 
    'Deposits & Withdrawals', 
    'Fees', 
    'Dividends', 
    'Withholding Tax', 
    'Interest', 
    'CYEP/Broker Fees', 
    'Payment In Lieu Of Dividends', 
    'Other Fees', 
    'Sales Tax Details', 
    'Broker Interest Paid',
    'Broker Interest Received', 
    'Bond Interest Paid', 
    'Bond Interest Received']

def check_and_parse_sections(df):
    """
    Checks if required sections exist in the CSV and parses them into separate DataFrames.
    
    :param df: Pandas DataFrame loaded from CSV
    :return: Dictionary of parsed DataFrames, one for each found section
    """
    parsed_sections = {}

    for section in REQUIRED_SECTIONS:
        if section in df.columns:  # Checking if section exists in column names
            parsed_sections[section] = df[[section]].dropna()  # Extract non-null data
            print(f"✅ Section found: {section}")
        else:
            print(f"⚠️ Section missing: {section}")

    return parsed_sections