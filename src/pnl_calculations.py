import pandas as pd
import re

FILTERED_COLS = ['Asset Category', 'Symbol', 'Amount', 'Underlying']

# Define different renaming rules
rename_rlzd = {'Realized Total': 'Amount'}
rename_vat = {'Sales Tax': 'Amount'}
rename_general = {'Currency':'Asset Category'}

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

expected_rows = {
    'Realized & Unrealized Performance Summary':['Stocks', 'Equity and Index Options', 'Forex', 'Bonds', 'Treasury Bills'], 
    'Dividends':['USD', 'Total in EUR'],
    'Withholding Tax':['USD', 'Total in EUR', 'Total Withholding Tax in EUR'],  
    'Bond Interest Received':['USD', 'Total', 'Total in EUR'],
    'Bond Interest Paid':['USD', 'Total', 'Total in EUR'], 
    'Broker Interest Received':['EUR', 'USD', 'Total Broker Interest Received in EUR'], 
    'Broker Interest Paid':['EUR', 'USD', 'Total in EUR'],
    'Other Fees':['Total'], 
    'Sales Tax Details':['Total'], 
    }

rename_dict2 = {'X': 'Xi', 'Y': 'Ypsilon', 'Z': 'Zeta'}
# Define new_rows dictionary
def new_rows(section_name, df):
    if section_name == 'Realized & Unrealized Performance Summary':
        df["Underlying"] = df["Symbol"].apply(extract_underlying)
    else:
        df["Symbol"] = df["Description"].apply(extract_underlying)
        df["Underlying"] = df["Description"].apply(extract_underlying)
    
    return df

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

def create_header(df):
    df.columns = df.iloc[0]  # Set first row as column names
    df = df[1:].reset_index(drop=True)  # Remove the first row and reset index  
    return df

def convert_to_numeric(df, col_name):
    df[col_name] = pd.to_numeric(df[col_name], errors='coerce', )  # Ensure numeric values
    return df

def pnl_constructor(lst, section_name):
    df = pd.DataFrame(lst)
    df = create_header(df)
    df.rename(columns=rename_dict[section_name], inplace=True)

    df = new_rows(section_name, df)

    filtered = df[df['Asset Category'].isin(expected_rows[section_name])] # Filter the rows to include only the expected_rows
    filtered = filtered.loc[:, [section_name] + FILTERED_COLS] # Filter the columns to include only the expected_cols
    
    filtered = convert_to_numeric(filtered, 'Amount')
    print(filtered.columns)
    return filtered
