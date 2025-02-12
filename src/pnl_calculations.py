import pandas as pd

def rlzd(lst):
    expected_rows = ['Stocks', 'Equity and Index Options', 'Forex', 'Bonds', 'Treasury Bills']
    expected_cols = ['Asset Category', 'Symbol', 'Realized Total']
    df = pd.DataFrame(lst)
    df.columns = df.iloc[0]  # Set first row as column names
    df = df[1:].reset_index(drop=True)  # Remove the first row and reset index
    filtered = df[df['Asset Category'].isin(expected_rows)]
    filtered = filtered.loc[:, expected_cols]
     
    return filtered

def dividends(lst):
    
    return

def whtax(lst):
    return

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