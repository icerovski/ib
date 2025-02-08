# Handles CSV file parsing
import csv
import pandas as pd

from collections import defaultdict
from src.data_selection import REQUIRED_SECTIONS

def parse_data(file_path):
    section_headers = {}
    section_records = defaultdict(list)  # key: section name, value: list of row dicts
    processed_sections = set()  # Track processed sections

    parsing_current_section = None # e.g. "Net Asset Value"

    with open(file_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)

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
            if section_name not in REQUIRED_SECTIONS:
                continue                    
            
            row_type = row[1].strip()
            fields = row[2:]  # everything after the first two columns

            if row_type.lower() == "header":
                # Store current section's header only if this is the first occurance of the section, i.e. Dividends
                if section_name in processed_sections:
                    parsing_current_section = False
                    continue
                else:
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
        section_dataframes[section] = df

    return section_dataframes