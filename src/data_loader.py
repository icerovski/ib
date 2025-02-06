# Handles CSV file parsing

import os
import pandas as pd
import csv

from src.calculations import get_file_path

def parse_nonstandard_csv(filename):
    file_path = get_file_path(filename, 'data', 'raw')
    print(f"🔍 Looking for file at: {file_path}")  # DEBUG OUTPUT
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")  # Show full path in error

    """
    Parse a CSV file that is broken into sections (column 0) and row-types (column 1).
    Each new 'Header' row begins a new sub-table within that section.
    Returns a dictionary like:
      {
        'Statement': [df1, df2, ...],
        'Account Information': [...],
        'Net Asset Value': [...],
        ...
      }
    where each element in the list is a pandas DataFrame corresponding to one header block.
    """
    sections = {}
    
    # Read the file as raw rows first
    with open(file_path, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    current_section_name = None       # e.g. "Net Asset Value"
    current_header = None             # list of header column names
    current_data_rows = []            # list of dicts (one per data row) for the current sub-table
    
    def save_current_subtable():
        """Helper: convert current_data_rows to a DataFrame using current_header,
        store it into the sections dict."""
        if not current_data_rows or not current_header:
            return
        
        # Because data rows can have more columns than the header, let's unify columns:
        # 1) Keep all columns from current_header
        # 2) Also keep any "Extra_1" or so from data dicts
        # 3) For missing columns, fill with None
        all_keys = set(current_header)  # from the last known header
        for rowdict in current_data_rows:
            all_keys.update(rowdict.keys())
        all_keys = list(all_keys)  # stable ordering

        # Convert list-of-dicts to DataFrame
        df = pd.DataFrame(current_data_rows, columns=all_keys)
        
        # Append the DataFrame into the right section list
        if current_section_name not in sections:
            sections[current_section_name] = []
        sections[current_section_name].append(df)

    for row in rows:
        # Basic sanity check: make sure row has at least 2 columns
        if len(row) < 2:
            continue  # skip blank or malformed lines
        
        section_name = row[0].strip()
        row_type = row[1].strip()
        remainder = row[2:]  # the columns after the first two

        if row_type == "Header":
            # If we already had a header & data building up, save it
            save_current_subtable()
            
            # Start a new "header" block
            current_section_name = section_name
            current_header = remainder
            current_data_rows = []
            
        else:
            # It's "Data", "Total", or some other row type
            # We'll slot it into the current header
            if not current_header:
                # There's no current header to match these data columns.
                # You might skip or handle differently.  We'll skip for safety.
                continue
            
            # Build a dict row keyed by the current_header.  If there are more
            # items than the header, store them in "Extra_1", "Extra_2", etc.
            row_dict = {}
            for i, val in enumerate(remainder):
                if i < len(current_header):
                    row_dict[current_header[i]] = val
                else:
                    # Extra columns beyond the header
                    extra_col_name = f"Extra_{i - len(current_header) + 1}"
                    row_dict[extra_col_name] = val
            
            # If the remainder has *fewer* columns than the header, fill None for missing
            if len(remainder) < len(current_header):
                for j in range(len(remainder), len(current_header)):
                    row_dict[current_header[j]] = None

            current_data_rows.append(row_dict)

    # End of file, save any leftover table
    save_current_subtable()

    return sections