import os
import pandas as pd
from collections import defaultdict
import streamlit as st
import csv

# pd.set_option('display.max_rows', None) # This is used in Jupiter to show all rows of the dataframe
def convert_to_numeric(df, col_name):
    df[col_name] = pd.to_numeric(df[col_name], errors='coerce')  # Ensure numeric values
    return df

def summarize_section(df, group_col, cash_col):
    temp_df = convert_to_numeric(df, cash_col) # Ensure numeric values
    summary = temp_df.groupby(group_col)[cash_col].sum().reset_index()
    return summary

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
    'Broker Interest Received', 
    'Bond Interest Paid', 
    'Bond Interest Received']


# Load the file as raw text to examine its structure
# with open(file_path, 'r') as file:
#     raw_content = file.readlines()
with open(file_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = []
    max_length = 0

    for row in reader:
        data.append(row)
        max_length = max(max_length, len(row))  # Track the longest row length

# Parse the content into sections and filter only required ones
filtered_sections = defaultdict(list) # Initialize dictionary to store data
section_headers = {} # Initialize dictionary to store headers
instrument_information_list = []
for line in data:
    # parts = [part.strip() for part in line.strip().split(',')]
    if line:
        section_name = line[0]
        if section_name in REQUIRED_SECTIONS:
            if line[1].lower() == 'header':
                section_headers[section_name] = line[2:] # Store the header row
            else:
                filtered_sections[section_name].append(line[2:]) # Append data rows to the filtered sections

        elif section_name == 'Financial Instrument Information':
            instrument_information_list.append(line[1:])

# Financial Instruments Information
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


sections_dict = {
    'Realized & Unrealized Performance Summary': ['Asset Category', 'Realized Total', CATEGORIES],
    'Dividends': ['Currency', 'Amount', 'Total in EUR'],
    'Withholding Tax': ['Currency', 'Amount', 'Total Withholding Tax in EUR'],
    'CYEP/Broker Fees': ['Currency', 'Amount', 'Total CYEP/Broker Fees in EUR'],
    'Bond Interest Received': ['Currency', 'Amount', 'Total in EUR'],
    'Bond Interest Paid': ['Currency', 'Amount', 'Total in EUR'],
    'Broker Interest Received': ['Currency', 'Amount', 'Total Broker Interest Received in EUR'],
    'Broker Interest Paid': ['Currency', 'Amount', 'Total in EUR'],
    'Other Fees': ['Currency', 'Amount', 'Total'],
    'Sales Tax Details': ['Currency', 'Sales Tax', 'Total'],
}

for section, values in sections_dict.items():
    df = pd.DataFrame(section_dataframes[section])
    summary = summarize_section(df, values[0], values[1])
    st.subheader(section)
    summary

# # Capital gains, USD ()
# current_df = pd.DataFrame(section_dataframes['Realized & Unrealized Performance Summary'])
# # convert_to_numeric(current_df, 'Realized Total')
# # summary = current_df.groupby("Asset Category")["Realized Total"].sum().reset_index()
# summary = summarize_section(current_df, 'Asset Category', 'Realized Total') 
# summary
# print(summary)

# # Dividends, EUR
# current_df = pd.DataFrame(section_dataframes['Dividends'])
# convert_to_numeric(current_df, 'Amount')
# summary = current_df.groupby("Currency")["Amount"].sum().reset_index()
# summary
# print(summary)

# # Withholding Tax
# current_df = pd.DataFrame(section_dataframes['Withholding Tax'])
# convert_to_numeric(current_df, 'Amount')
# summary = current_df.groupby("Currency")["Amount"].sum().reset_index()
# summary
# print(summary)

# # Bond Interest Received
# current_df = pd.DataFrame(section_dataframes['Bond Interest Received'])
# convert_to_numeric(current_df, 'Amount')
# summary = current_df.groupby("Currency")["Amount"].sum().reset_index()
# summary
# print(summary)

# # Bond Interest Paid
# current_df = pd.DataFrame(section_dataframes['Bond Interest Paid'])
# convert_to_numeric(current_df, 'Amount')
# summary = current_df.groupby("Currency")["Amount"].sum().reset_index()
# summary
# print(summary)

# # Broker Interest Received
# current_df = pd.DataFrame(section_dataframes['Broker Interest Received'])
# convert_to_numeric(current_df, 'Amount')
# summary = current_df.groupby("Currency")["Amount"].sum().reset_index()
# summary
# print(summary)

# # Broker Interest Paid
# current_df = pd.DataFrame(section_dataframes['Broker Interest Paid'])
# convert_to_numeric(current_df, 'Amount')
# summary = current_df.groupby("Currency")["Amount"].sum().reset_index()
# summary
# print(summary)

# # CYEP/Broker Fees
# current_df = pd.DataFrame(section_dataframes['CYEP/Broker Fees'])
# convert_to_numeric(current_df, 'Amount')
# summary = current_df.groupby("Currency")["Amount"].sum().reset_index()
# summary
# print(summary)

# # Other Fees
# current_df = pd.DataFrame(section_dataframes['Other Fees'])
# convert_to_numeric(current_df, 'Amount')
# summary = current_df.groupby("Currency")["Amount"].sum().reset_index()
# summary
# print(summary)

# # Sales Tax Details
# current_df = pd.DataFrame(section_dataframes['Sales Tax Details'])
# current_df
# convert_to_numeric(current_df, 'Sales Tax')
# summary = current_df.groupby("Currency")["Sales Tax"].sum().reset_index()
# summary
# print(summary)

# filt_row = rlzd_df['Asset Category'].isin(CATEGORIES)
# filt_col = ['Asset Category', 'Symbol', 'Realized Total']
# filtered_rlzd = rlzd_df.loc[filt_row, filt_col]


# Streamlit interactive table
# cmd> streamlit run report.py
# Ctr+Shift+` to add a new terminal (cmd) where you can continue to run/test the script as per usual

# Python environment activation
# 1. go to project environment folder (ib)
# 2. bash: deactivate
# 3. bash: pipenv shell