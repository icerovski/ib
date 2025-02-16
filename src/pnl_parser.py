# Handles CSV file parsing
import csv
import pandas as pd

from collections import defaultdict
from src.pnl_calculations import pnl_constructor
from src.streamlit_viewer import display_df

PNL_SECTIONS = [
    'Realized & Unrealized Performance Summary', 
    'Dividends', 
    'Withholding Tax',  
    'Bond Interest Received',
    'Bond Interest Paid', 
    'Broker Interest Received', 
    'Broker Interest Paid',
    'Other Fees', 
    'Sales Tax Details', 
    ]

def zero_df(section_name):
    zero_dict = {
        'Asset Category':section_name, 'Symbol': None, 'Amount': [0], 'Underlying': None
        }

    return pd.DataFrame(zero_dict)

RENAME_DICT = {
    "Realized Total": "Amount",  # Correcting typo
    "Sales Tax": "Amount"
    }

def isolate_section(reader, section_name):
    # Identify the start and end of the current section
    start_idx = None
    end_idx = None

    # iterate over the rows while keeping track of both the index (i) and the actual content of each row (row)
    # enumerate assigns an index (i) to each row
    
    # Search for section start
    for i, row in enumerate(reader):
        # Check the first column of each row for the section name
        if section_name in row[0] and start_idx is None:
            start_idx = i
        elif start_idx is not None and section_name not in row[0] and ",Data," not in row[1]:
            end_idx = i
            break
 
    if start_idx is None:
        # We raise ValueError if the section isn’t found
        raise ValueError(f"Section '{section_name}' not found in file.")
    
    return reader[start_idx:end_idx] # Extract only the relevant section if found by slicing the list

def pnl_parser(file_path):
    # parsing_current_section = None # e.g. "Net Asset Value"
    final_result = []

    with open(file_path, "r", newline="") as csvfile:

        reader = list(csv.reader(csvfile)) # csv.reader returns an iterator -> convert iterator to list
        
        section_rows = []        

        for section_name in PNL_SECTIONS:
            section_rows.clear()

            # Sometimes not all sections are present, i.e. some months I don't trade any Treasury Bills. Handle the exception gracefully.
            try:
                section_rows = isolate_section(reader, section_name)
            except ValueError as e:
                print(f"Warning: {e}. Using zero P&L.")
                section_rows = []

            if not section_rows:
                current_pnl_df = zero_df(section_name)
            else:
                # current_pnl_df = func(section_rows, section_name)
                current_pnl_df = pnl_constructor(section_rows, section_name)
        
            # Add current pnl DataFrame to a summary list
            final_result.append(current_pnl_df)
            display_df(section_name, current_pnl_df)

    return pd.concat(final_result)

