import pandas as pd
import re

RENAME_DICT = {
    "Realized Total": "Amount",  # Correcting typo
    "Sales Tax": "Amount"
}

def create_header(df):
    df.columns = df.iloc[0]  # Set first row as column names
    df = df[1:].reset_index(drop=True)  # Remove the first row and reset index  
    return df

def add_col_to_df(df, source_col, new_col):
    '''
    Extract the underlying from the Symbol column and add a new column with the underlying
    '''
    # underlying = df[col_name].str.extract(r'([A-Z]+)')

    # Adjust regex to capture single capital letters and alphanumeric combinations like "4GLD"
    df[new_col] = df[source_col].str.extract(r'^([A-Z0-9]+)')
    return

def convert_to_numeric(df, col_name):
    df[col_name] = pd.to_numeric(df[col_name], errors='coerce', )  # Ensure numeric values
    return df

def rlzd(lst):
    df = pd.DataFrame(lst)
    df = create_header(df)
    df.rename(columns=RENAME_DICT, inplace=True)
    
    add_col_to_df(df, 'Symbol', 'Underlying')
    
    # Convert amounts to numeric
    df = convert_to_numeric(df, 'Amount')
    
    expected_rows = ['Stocks', 'Equity and Index Options', 'Forex', 'Bonds', 'Treasury Bills']
    expected_cols = ['Asset Category', 'Symbol', 'Amount', 'Underlying']
    
    filtered = df[df['Asset Category'].isin(expected_rows)] # Filter the rows to include only the expected_rows
    filtered = filtered.loc[:, expected_cols] # Filter the columns to include only the expected_cols
    
    print(filtered.head())
    return filtered

def dividends(lst):
    df = pd.DataFrame(lst)
    df = create_header(df)
    df.rename(columns={'Currency':'Asset Category'}, inplace=True)
 
    add_col_to_df(df, 'Description', 'Symbol')
    add_col_to_df(df, 'Description', 'Underlying')

    # Convert amounts to numeric
    df = convert_to_numeric(df, 'Amount')
    
    expected_rows = ['USD', 'Total in EUR']
    expected_cols = ['Asset Category', 'Symbol', 'Amount', 'Underlying']

    filtered = df[df['Asset Category'].isin(expected_rows)] # Filter the rows to include only the expected_rows
    filtered = filtered.loc[:, expected_cols] # Filter the columns to include only the expected_cols
    
    print(filtered.head())
    return filtered

def whtax(lst):
    df = pd.DataFrame(lst)
    df = create_header(df)
    df.rename(columns={'Currency':'Asset Category'}, inplace=True)
 
    # add_col_to_df(df, 'Description', 'Symbol')
    # add_col_to_df(df, 'Description', 'Underlying')
    # Extract the underlying ticker by capturing text before the first "("
    df["Underlying"] = df["Description"].str.extract(r'^([^(\s]+)\(')
    df["Symbol"] = df["Description"].str.extract(r'^([^(\s]+)\(')
    
    # Convert amounts to numeric
    df = convert_to_numeric(df, 'Amount')
    
    expected_rows = ['USD', 'Total in EUR', 'Total Withholding Tax in EUR']
    expected_cols = ['Asset Category', 'Symbol', 'Amount', 'Underlying']

    filtered = df[df['Asset Category'].isin(expected_rows)] # Filter the rows to include only the expected_rows
    filtered = filtered.loc[:, expected_cols] # Filter the columns to include only the expected_cols
    
    print(filtered.head())
    return filtered

def bond_interest_received(lst):
    return

def bond_interest_paid(lst):
    return

def broker_interest_received(lst):
    return

def broker_interest_paid(lst):
    return

def other_fees(lst):
    return

def sales_tax(lst):
    return