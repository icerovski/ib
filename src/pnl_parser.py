# Handles CSV file parsing
import csv
import pandas as pd

from collections import defaultdict
from src.pnl_calculations import rlzd, dividends, whtax, bond_interest_received, bond_interest_paid, broker_interest_received, broker_interest_paid, other_fees, sales_tax
from src.streamlit_viewer import display_df

# PNL_SECTIONS = [
#     'Realized & Unrealized Performance Summary', 
#     'Dividends', 
#     'Withholding Tax',  
#     'Bond Interest Received',
#     'Bond Interest Paid', 
#     'Broker Interest Received', 
#     'Broker Interest Paid',
#     'Other Fees', 
#     'Sales Tax Details', 
#     ]

pnl_functions = {
    'Realized & Unrealized Performance Summary':rlzd, 
    'Dividends':dividends, 
    'Withholding Tax':whtax,  
    'Bond Interest Received':bond_interest_received,
    'Bond Interest Paid':bond_interest_paid, 
    'Broker Interest Received':broker_interest_received, 
    'Broker Interest Paid':broker_interest_paid,
    'Other Fees':other_fees, 
    'Sales Tax Details':sales_tax, 
}

DO_NOT_REPEAT = [
    'Dividends'
]

RENAME_DICT = {
    "Realized Total": "Amount",  # Correcting typo
    "Sales Tax": "Amount"
}



def pnl_parser(file_path):
    section_headers = {}
    section_records = defaultdict(list)  # key: section name, value: list of row dicts
    processed_sections = set()  # Track processed sections

    parsing_current_section = None # e.g. "Net Asset Value"

    with open(file_path, "r", newline="") as csvfile:

        def isolate_section(str):
            # Identify the start and end of the current section
            start_idx = None
            end_idx = None
            section_rows = []

            # iterate over the rows while keeping track of both the index (i) and the actual content of each row (row)
            # enumerate assigns an index (i) to each row
            for i, row in enumerate(reader):
                if section_name in row and start_idx is None:
                    start_idx = i
                elif start_idx is not None and section_name not in row and ",Data," not in row:
                    end_idx = i
                    break

            section_rows = reader[start_idx:end_idx] # Extract only the relevant section if found by slicing the list
            
            return section_rows

        reader = list(csv.reader(csvfile)) # csv.reader returns an iterator -> convert iterator to list        
        for section_name, func in pnl_functions.items():
            # Sometimes not all sections are present, i.e. some months I don't trade any Treasury Bills. Handle the exception gracefully.
            try:
                section_rows = isolate_section(section_name)
            except ValueError:
                print(f"Warning: {section_name} section not found. Returning empty DataFrame.")
                return pd.DataFrame()  # Or handle it differently

            current_pnl_df = func(section_rows)
            display_df(section_name, current_pnl_df)




        def save_current_row():
            # Hint: pair each header column with its corresponding data value
            record = {}
            for col_name, col_value in zip(section_headers[section_name], fields):
                record[col_name.strip()] = col_value.strip()
            
            # Append to the list for this section
            section_records[section_name].append(record)
        
        for row in reader:
            if not row:
                continue
            
            # Parse current row
            section_name = row[0].strip()
            if section_name not in pnl_functions:
                continue                    
            
            row_type = row[1].strip()
            fields = row[2:]  # everything after the first two columns

            if row_type.lower() == "header":
                # Check if this is repeated appearance for this section, i.e. Dividends or Financial Instrument Information
                if section_name in processed_sections:
                    # Check if section is in the REPEATED list and needs to be parsed only once
                    if section_name in DO_NOT_REPEAT: 
                        parsing_current_section = False
                else:
                    # Store current section's header only if this is the first occurance of the section, i.e. Dividends
                    processed_sections.add(section_name) # Mark the section as processed, so that it no longer gets processed
                    section_headers[section_name] = fields # Store the current section's header
                    parsing_current_section = True
                
            elif row_type.lower() == "data":
                # Process only sections that do not repeat
                if parsing_current_section:
                    save_current_row()

    return section_records

def convert_to_dataframe(section_records):
    # Convert each section’s list of dictionaries into its own DataFrame
    section_dataframes = {}
    for section, records_list in section_records.items():
        # section is the dictionary key
        # records_list is the list of row dictionaries
        df = pd.DataFrame(records_list)
        # Rename some of the value headers to Amount so they are similar with all other dataframes
        df.rename(columns=RENAME_DICT, inplace=True)
        section_dataframes[section] = df

    return section_dataframes