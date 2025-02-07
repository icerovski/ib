# Handles CSV file parsing
import csv
import pandas as pd

from collections import defaultdict
from src.data_selection import REQUIRED_SECTIONS

def parse_data(file_path):
    section_headers = {}
    section_records = defaultdict(list)  # key: section name, value: list of row dicts

    with open(file_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if not row:
                continue
            
            section_name = row[0].strip()
            row_type = row[1].strip()
            fields = row[2:]  # everything after the first two columns

            # You might choose to skip or handle missing headers differently
            if section_name not in REQUIRED_SECTIONS:
                continue

            if row_type.lower() == "header":
                # Hint: store the current section’s headers
                section_headers[section_name] = fields

            elif row_type.lower() == "data":
                # Retrieve headers for the current section (if available)
                if section_name not in section_headers:
                    # You might choose to skip or handle missing headers differently
                    continue
                                
                # Hint: pair each header column with its corresponding data value
                record = {}
                for col_name, col_value in zip(section_headers[section_name], fields):
                    record[col_name.strip()] = col_value.strip()
                
                # Append to the list for this section
                section_records[section_name].append(record)
    
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