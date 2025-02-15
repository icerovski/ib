import os
import pandas as pd
from collections import defaultdict
# import streamlit as st
import csv

# Import display to render DataFrames nicely in Jupyter cells
from IPython.display import display

# pd.set_option('display.max_rows', None) # This is used in Jupiter to show all rows of the dataframe
def convert_to_numeric(df, col_name):
    df[col_name] = pd.to_numeric(df[col_name], errors='coerce')  # Ensure numeric values
    return df

def summarize_section(df, group_col, cash_col):
    temp_df = convert_to_numeric(df, cash_col) # Ensure numeric values
    summary = temp_df.groupby(group_col)[cash_col].sum().reset_index()
    return summary

def pull_data(source_file, criterion):
    data = []
    with open(str(source_file), 'r') as source_file:
        reader = csv.reader(source_file, delimiter= ',')
        for row in reader:
            if row[0] == criterion:
                data.append(row[1:])
    return data

def parse_multiheader_csv(filename):
    """
    Reads a CSV file where:
      - Col 0 = Section Name
      - Col 1 = Type (e.g. 'Header' or 'Data')
      - Remaining cols = either actual header fields or data fields

    Returns a dictionary:
      {
        "SectionName": [
            ("HeaderName/FirstColumnOfHeader", pandas.DataFrame),
            ...
        ],
        ...
      }
    """
    # This dictionary will map section -> list of (header_label, DataFrame)
    result = {}

    with open(filename, newline='') as f:
        reader = csv.reader(f)

        current_section = None
        current_header = None
        current_header_label = None
        current_data_rows = []

        for row in reader:
            # Skip empty or malformed rows
            if len(row) < 2:
                continue

            section, row_type = row[0], row[1]

            # If we have changed sections, close out the old sub-table if needed
            if section != current_section:
                # Store the old sub-table in result
                if current_section is not None and current_header and current_data_rows:
                    df = pd.DataFrame(current_data_rows, columns=current_header)
                    result[current_section].append((current_header_label, df))
                
                # Initialize for the new section
                current_section = section
                if current_section not in result:
                    result[current_section] = []

                current_header = None
                current_header_label = None
                current_data_rows = []

            # If this is a new header row, start a new sub-table
            if row_type == 'Header':
                # If there was a sub-table in progress, store it
                if current_header and current_data_rows:
                    df = pd.DataFrame(current_data_rows, columns=current_header)
                    result[current_section].append((current_header_label, df))

                # Grab the new header fields
                current_header = row[2:]
                
                # You can define the sub-table's "label" from the header itself
                if current_header:
                    current_header_label = current_header[0]
                else:
                    current_header_label = "UnnamedHeader"

                # Reset data rows for this sub-table
                current_data_rows = []

            elif row_type == 'Data':
                # This is a data row for the current sub-table
                data_fields = row[2:]

                # Make sure we actually have a header to map to
                if current_header:
                    header_len = len(current_header)
                    row_len = len(data_fields)

                    if row_len < header_len:
                        # Pad with empty strings
                        data_fields += [""] * (header_len - row_len)
                    elif row_len > header_len:
                        # Trim extra columns
                        data_fields = data_fields[:header_len]
                    
                    current_data_rows.append(data_fields)
                else:
                    # If no header, you might decide to skip or handle differently
                    pass

        # End of file: if there's an unfinished sub-table, store it
        if current_header and current_data_rows:
            df = pd.DataFrame(current_data_rows, columns=current_header)
            result[current_section].append((current_header_label, df))

    return result

def main():
    # File path to the uploaded CSV
    # month_input = input('Provide YYYYMM:')
    # ib_file_name = 'U16432685' + '_' + month_input + '_' + month_input + ".csv"
    
    # ib_file_name = 'U16432685_20240101_20241231.csv'
    ib_file_name = 'U16432685_202501_202501.csv'
    # ib_file_name = 'MULTI_20240101_20241231.csv'
    script_dir = os.path.dirname(os.path.abspath(__file__)) # Get the directory where the script is located
    file_path = os.path.join(script_dir, ib_file_name) # Construct the full path to the CSV file

    parsed_data = parse_multiheader_csv(file_path)
    
    # 'parsed_data' is now a dictionary: { section: [(header_label, DataFrame), ...], ... }
    for section, tables in parsed_data.items():
        print(f"\n--- SECTION: {section} ---")
        for header_label, df in tables:
            print(f"Header Label: {header_label}")
            # print(df)
            # print()

    print('These were all the Sections')

    # Dictionary to hold section DataFrames
    sections = {}

    # Variables to track the current section name and its data rows
    current_section = None
    current_data = []


    # Open the CSV file in read mode
    with open(file_path, 'r') as f:
        # Process each line in the file
        for line in f:
            # Remove any extra whitespace/newlines and split by comma
            row = line.strip().split(',')
            
            # Replace the condition below with your logic to detect a section start
            if row[0].startswith('SECTION_MARKER'):  # Hint: define your marker here
                # If data for the previous section exists, create a DataFrame
                if current_section and current_data:
                    # Assume first row is header, rest are data rows
                    df = pd.DataFrame(current_data[1:], columns=current_data[0])
                    sections[current_section] = df
                # Start a new section
                current_section = row[0]  # You may want to adjust how you name sections
                current_data = [row]  # Begin collecting rows for this new section
            else:
                # Continue collecting rows for the current section
                current_data.append(row)
        
            # After looping, handle the final section if present
        if current_section and current_data:
            df = pd.DataFrame(current_data[1:], columns=current_data[0])
            sections[current_section] = df

    # Loop through your dictionary of DataFrames (assumed to be named 'sections')
    for section_name, df in sections.items():
        # Print out the section name so you know which DataFrame you're looking at
        print(f"Section: {section_name}")
        # Use display() to render the DataFrame as an interactive table
        display(df)



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

    # st.subheader(f"Taxed Stocks")
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
        # 'CYEP/Broker Fees': ['Currency', 'Amount', 'Total CYEP/Broker Fees in EUR'],
        'Bond Interest Received': ['Currency', 'Amount', 'Total in EUR'],
        # 'Bond Interest Paid': ['Currency', 'Amount', 'Total in EUR'],
        'Broker Interest Received': ['Currency', 'Amount', 'Total Broker Interest Received in EUR'],
        'Broker Interest Paid': ['Currency', 'Amount', 'Total in EUR'],
        'Other Fees': ['Currency', 'Amount', 'Total'],
        'Sales Tax Details': ['Currency', 'Sales Tax', 'Total'],
    }

    for section, values in sections_dict.items():
        df = pd.DataFrame(section_dataframes[section])
        summary = summarize_section(df, values[0], values[1])
        # st.subheader(section)
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

if __name__ == "__main__":
    main()