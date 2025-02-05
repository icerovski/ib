import os
import pandas as pd
from collections import defaultdict
import streamlit as st

# pd.set_option('display.max_rows', None) # This is used in Jupiter to show all rows of the dataframe

# File path to the uploaded CSV
# ib_file_name = 'U8432685_20240101_20241028.csv'
ib_file_name = 'MULTI_20240101_20241231.csv'
script_dir = os.path.dirname(os.path.abspath(__file__)) # Get the directory where the script is located
file_path = os.path.join(script_dir, ib_file_name) # Construct the full path to the CSV file

# CONSTANTS
CATEGORIES = ["Stocks", "Equity and Index Options", "Forex", "Bonds", "Treasury Bills"]

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
    'Bond Interest Paid', 
    'Bond Interest Received']

# Load the file as raw text to examine its structure
with open(file_path, 'r') as file:
    raw_content = file.readlines()

# Parse the content into sections and filter only required ones
filtered_sections = defaultdict(list) # Initialize dictionary to store data
section_headers = {} # Initialize dictionary to store headers
instrument_information_list = []
for line in raw_content:
    parts = [part.strip() for part in line.strip().split(',')]
    if parts:
        section_name = parts[0]
        if section_name in REQUIRED_SECTIONS:
            if parts[1].lower() == 'header':
                section_headers[section_name] = parts[2:] # Store the header row
            else:
                filtered_sections[section_name].append(parts[2:]) # Append data rows to the filtered sections

        elif section_name == 'Financial Instrument Information':
            instrument_information_list.append(parts[1:])

# Convert Financial Instrument Information list to two dictionaries
max_length = max(len(row) for row in instrument_information_list)
for row in instrument_information_list:
    while len(row) < max_length:
        row.append('')

instruments_df = pd.DataFrame(instrument_information_list[1:], columns=instrument_information_list[0])

# Clean up rows
instruments_df = instruments_df[instruments_df['Header'] != 'Header'] # Filter out rows where 'Header' is "Header"
instruments_df.drop_duplicates(subset=['Symbol'], inplace=True)

# Clean up the columns
instrument_info = ['Asset Category', 'Symbol', 'Description', 'Listing Exch', 'Type']
instruments_df = instruments_df[instrument_info]

# Create a filter for taxable stocks
is_common = (instruments_df['Type'] == 'COMMON')
is_treasury = (instruments_df['Asset Category'] == 'Treasury Bills')
is_european = (instruments_df['Listing Exch'].isin(['SBF', 'IBIS', 'IBIS2']))
tax_exempt = is_common | is_treasury | is_european

taxed_stocks = instruments_df.loc[~tax_exempt, ['Asset Category', 'Symbol', 'Description', 'Listing Exch', 'Type']]

# Sort the rows first by Asset Category descending then by Symbol ascending
taxed_stocks.sort_values(by=['Asset Category', 'Symbol'], ascending=[False, True], inplace=True)
taxed_stocks.reset_index()
print(taxed_stocks.shape)

st.subheader(f"Taxed Stocks")
taxed_stocks # st.dataframe(taxed_stocks)

# Convert filtered sections to DataFrames for structured processing
section_dataframes = {}
for section, data in filtered_sections.items():
    headers = section_headers.get(section, []) # Populate the headers dictionary
    section_dataframes[section] = pd.DataFrame(data, columns=headers) # Populate the section dictionary as a dataframe

    # st.subheader(f"Section: {section}")
    # st.dataframe(section_dataframes[section])

# Capital gains, USD ()
rlzd_df = pd.DataFrame(section_dataframes['Realized & Unrealized Performance Summary'])
rlzd_df

print(rlzd_df.loc[:, ['Realized Total']].dtypes)

filt_row = rlzd_df['Asset Category'].isin(CATEGORIES)
filt_col = ['Asset Category', 'Symbol', 'Realized Total']
filtered_rlzd = rlzd_df.loc[filt_row, filt_col]
print(filtered_rlzd.dtypes)

# Group by 'Asset Category' and calculate the sum of 'Realized Total'
filt = filtered_rlzd.groupby(['Asset Category']).sum()
category_profit = filt.loc[:, 'Realized Total']
category_profit
# category_sum.reset_index() # resets the index order to start from zero, because after filtering it got mixed up
# category_sum

# Rename the Total cells
# filt_row = (rlzd_df['Asset Category'] == 'Total')
# filt_col = ['Asset Category']
# filtered_rlzd = rlzd_df.loc[filt_row, filt_col]
# filtered_rlzd.str.lower()



# Streamlit interactive table
# cmd> streamlit run report.py
# Ctr+Shift+` to add a new terminal (cmd) where you can continue to run/test the script as per usual

# Python environment activation
# 1. go to project environment folder (ib)
# 2. bash: deactivate
# 3. bash: pipenv shell