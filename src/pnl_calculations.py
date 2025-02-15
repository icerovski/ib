import pandas as pd
import re

FILTERED_COLS = ['Asset Category', 'Symbol', 'Amount', 'Underlying']

# Define different renaming rules
rename_rlzd = {'Realized Total': 'Amount'}
rename_vat = {'Sales Tax': 'Amount'}
rename_general = {'Currency':'Asset Category'}

def rename_columns(df, rename_dict):
    """
    Renames columns in a DataFrame based on a given dictionary.
    
    :param df: The DataFrame to rename columns for.
    :param rename_dict: A dictionary where keys are old column names and values are new names.
    :return: The DataFrame with renamed columns.
    """
    return df.rename(columns=rename_dict)

rename_dict = {
    'Realized & Unrealized Performance Summary':rename_rlzd, 
    'Dividends':rename_general,
    'Withholding Tax':rename_general,  
    'Bond Interest Received':rename_general,
    'Bond Interest Paid':rename_general, 
    'Broker Interest Received':rename_general, 
    'Broker Interest Paid':rename_general,
    'Other Fees':rename_general, 
    'Sales Tax Details':rename_general | rename_vat, 
    }

rename_dict2 = {'X': 'Xi', 'Y': 'Ypsilon', 'Z': 'Zeta'}

# Define a function to extract the correct ticker based on different asset types
def extract_underlying(description):
    # Case: Stocks (a single uppercase word with numbers, and nothing else in the field)
    stock_match = re.search(r'^\b[A-Z0-9]+\b$', description)
    if stock_match:
        return description

    # Case: Bonds (detects uppercase words followed by an interest rate AND an expiration date)
    bond_match = re.search(r'\b([A-Z]+)(?=\s(\d+\.\d{1,2}|\d+\s\d+/\d+)\s\d{2}/\d{2}/\d{2})', description)
    if bond_match:
        return bond_match.group(1)

    # Case: Dividends & WHTax (first uppercase letters before '(')
    div_whtax_match = re.search(r'^([^(\s]+)\(', description)
    if div_whtax_match:
        return div_whtax_match.group(1)

    # Case: RLZD & Broker (first uppercase letters and numbers before a space)
    space_match = re.search(r'^([A-Z0-9]+)\s', description)
    if space_match:
        return space_match.group(1)

    return None  # Return None if no match is found

def pnl_constructor(lst, section_name):
    df = pd.DataFrame(lst)
    df = create_header(df)


    return

def create_header(df):
    df.columns = df.iloc[0]  # Set first row as column names
    df = df[1:].reset_index(drop=True)  # Remove the first row and reset index  
    return df

def convert_to_numeric(df, col_name):
    df[col_name] = pd.to_numeric(df[col_name], errors='coerce', )  # Ensure numeric values
    return df

def rlzd(lst, section_name):
    df = pd.DataFrame(lst)
    df = create_header(df)

    rename_columns(df, rename_dict[section_name])  # Rename and update the dictionary
    df.rename(columns={"Realized Total": "Amount"}, inplace=True)
    
    print(df.head())
    df["Underlying"] = df["Symbol"].apply(extract_underlying)
    
    # Convert amounts to numeric
    df = convert_to_numeric(df, 'Amount')
    
    expected_rows = ['Stocks', 'Equity and Index Options', 'Forex', 'Bonds', 'Treasury Bills']
    
    filtered = df[df['Asset Category'].isin(expected_rows)] # Filter the rows to include only the expected_rows
    filtered = filtered.loc[:, [section_name] + FILTERED_COLS] # Filter the columns to include only the expected_cols
    
    print(filtered.head())
    return filtered

def dividends(lst, section_name):
    df = pd.DataFrame(lst)
    df = create_header(df)
    print(rename_dict.keys())
    rename_columns(df, rename_dict[section_name])  # Rename and update the dictionary
    print(df.head())
    df.rename(columns={'Currency':'Asset Category'}, inplace=True)

    df["Symbol"] = df["Description"].apply(extract_underlying)
    df["Underlying"] = df["Description"].apply(extract_underlying)

    # Convert amounts to numeric
    df = convert_to_numeric(df, 'Amount')
    
    expected_rows = ['USD', 'Total in EUR']

    filtered = df[df['Asset Category'].isin(expected_rows)] # Filter the rows to include only the expected_rows
    filtered = filtered.loc[:, [section_name] + FILTERED_COLS] # Filter the columns to include only the expected_cols
    
    print(filtered.head())
    return filtered

def whtax(lst, section_name):
    df = pd.DataFrame(lst)
    df = create_header(df)
    df.rename(columns={'Currency':'Asset Category'}, inplace=True)
 
    print(df.head())
    df["Symbol"] = df["Description"].apply(extract_underlying)
    df["Underlying"] = df["Description"].apply(extract_underlying)
    
    # Convert amounts to numeric
    df = convert_to_numeric(df, 'Amount')
    
    expected_rows = ['USD', 'Total in EUR', 'Total Withholding Tax in EUR']

    filtered = df[df['Asset Category'].isin(expected_rows)] # Filter the rows to include only the expected_rows
    filtered = filtered.loc[:, [section_name] + FILTERED_COLS] # Filter the columns to include only the expected_cols
    
    print(filtered.head())
    return filtered

def bond_interest_received(lst, section_name):
    df = pd.DataFrame(lst)
    df = create_header(df)
    df.rename(columns={'Currency':'Asset Category'}, inplace=True)
 
    print(df.head())
    df["Symbol"] = df["Description"].apply(extract_underlying)
    df["Underlying"] = df["Description"].apply(extract_underlying)
 
    # Convert amounts to numeric
    df = convert_to_numeric(df, 'Amount')
    
    expected_rows = ['USD', 'Total', 'Total in EUR']

    filtered = df[df['Asset Category'].isin(expected_rows)] # Filter the rows to include only the expected_rows
    filtered = filtered.loc[:, [section_name] + FILTERED_COLS] # Filter the columns to include only the expected_cols
    
    print(filtered.head())
    return filtered    

def bond_interest_paid(lst, section_name):
    df = pd.DataFrame(lst)
    df = create_header(df)
    df.rename(columns={'Currency':'Asset Category'}, inplace=True)
 
    print(df.head())
    df["Symbol"] = df["Description"].apply(extract_underlying)
    df["Underlying"] = df["Description"].apply(extract_underlying)
 
    # Convert amounts to numeric
    df = convert_to_numeric(df, 'Amount')
    
    expected_rows = ['USD', 'Total', 'Total in EUR']

    filtered = df[df['Asset Category'].isin(expected_rows)] # Filter the rows to include only the expected_rows
    filtered = filtered.loc[:, [section_name] + FILTERED_COLS] # Filter the columns to include only the expected_cols
    
    print(filtered.head())
    return filtered       

def broker_interest_received(lst, section_name):
    df = pd.DataFrame(lst)
    df = create_header(df)
    df.rename(columns={'Currency':'Asset Category'}, inplace=True)
 
    print(df.head())
    df["Symbol"] = df["Description"].apply(extract_underlying)
    df["Underlying"] = df["Description"].apply(extract_underlying)
 
    # Convert amounts to numeric
    df = convert_to_numeric(df, 'Amount')
    
    expected_rows = ['EUR', 'USD', 'Total Broker Interest Received in EUR']

    filtered = df[df['Asset Category'].isin(expected_rows)] # Filter the rows to include only the expected_rows
    filtered = filtered.loc[:, [section_name] + FILTERED_COLS] # Filter the columns to include only the expected_cols
    
    print(filtered.head())
    return filtered

def broker_interest_paid(lst, section_name):
    return

def other_fees(lst, section_name):
    df = pd.DataFrame(lst)
    df = create_header(df)
    df.rename(columns={'Currency':'Asset Category'}, inplace=True)
 
    print(df.head())
    df["Symbol"] = df["Description"].apply(extract_underlying)
    df["Underlying"] = df["Description"].apply(extract_underlying)
 
    # Convert amounts to numeric
    df = convert_to_numeric(df, 'Amount')
    
    expected_rows = ['Total']

    filtered = df[df['Asset Category'].isin(expected_rows)] # Filter the rows to include only the expected_rows
    filtered = filtered.loc[:, [section_name] + FILTERED_COLS] # Filter the columns to include only the expected_cols
    
    print(filtered.head())
    return filtered

def sales_tax(lst, section_name):
    df = pd.DataFrame(lst)
    df = create_header(df)
    df.rename(columns={'Currency':'Asset Category'}, inplace=True)
    df.rename(columns={"Sales Tax": "Amount"}, inplace=True)
 
    print(df.head())
    df["Symbol"] = df["Description"].apply(extract_underlying)
    df["Underlying"] = df["Description"].apply(extract_underlying)
 
    # Convert amounts to numeric
    df = convert_to_numeric(df, 'Amount')
    
    expected_rows = ['Total']

    filtered = df[df['Asset Category'].isin(expected_rows)] # Filter the rows to include only the expected_rows
    filtered = filtered.loc[:, [section_name] + FILTERED_COLS] # Filter the columns to include only the expected_cols
    
    print(filtered.head())
    return filtered