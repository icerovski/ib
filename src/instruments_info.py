import csv
from collections import defaultdict
import pandas as pd

INFO_SECTION = 'Financial Instrument Information'

# INSTRUMENT_MAPPING = {
#     'Realized & Unrealized Performance Summary': 'Symbol',
#     'Dividends': 'Description',
#     'Withholding Tax': 'Description',
#     'Bond Interest Received': 'Description',
#     'Bond Interest Paid': 'Description',
#     'Broker Interest Received': 'Description',
#     'Broker Interest Paid': 'Description',
# }

COLUMNS_TO_KEEP = [
    'Asset Category',
    'Symbol',
    'Underlying',
    'Listing Exch',
    'Type'
]

def add_col_underlying(df_dict):
    for section, col_name in INSTRUMENT_MAPPING.items():
        if section in df_dict:
            current_section = df_dict[section]
            current_underlying = current_section[col_name].str.extract(r'([A-Z]+)') 
            current_section['Underlying'] = current_underlying
    
    return

def extract_underlying(section, col_name):
    # Extract underlying names using regex
    # current_underlying = current_section[col_name].str.extract(r'([A-Z]+)') 
    section['Underlying'] = section[col_name].astype(str).str.extract(r'([A-Z]+)')
    selection = section.loc[:, ['Underlying', 'Type']]
    print(selection)
    # df_cleaned = section.
        
    # Create a set of unique underlying names
    unique_underlyings = set(section["Underlying"].dropna().unique())

    return unique_underlyings

def filter_and_move_to_list_of_df(curr_l, df_l):
        df = pd.DataFrame(curr_l)
        df_l.append(df.loc[:, COLUMNS_TO_KEEP]) # Keep only the required columns in the DataFrame and append it to a list of dataframes
    

def parse_info_section(file_path):
    parsing_current_asset_category = None # Skip the first iterration of the headers

    with open(file_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        df_list = [] # List of DataFrames

        def save_current_row():
            # Hint: pair each header column with its corresponding data value
            record = {}
            for col_name, col_value in zip(headers, fields):
                record[col_name.strip()] = col_value.strip()
            
            print(type(record))
            # Append to the main dictionary
            current_records.append(record)

        for row in reader:
            if not row:
                continue
            
            # Parse current row
            section_name = row[0].strip()
            if section_name != INFO_SECTION:
                continue                    
            
            row_type = row[1].strip()
            fields = row[2:]  # everything after the first two columns
            
            # if parsing_current_asset_category:
            #     asset_category = row[2].strip()

            if row_type.lower() == "header":
                if parsing_current_asset_category:
                    # df = pd.DataFrame(current_records)
                    # df_list.append(df.loc[:, COLUMNS_TO_KEEP]) # Keep only the required columns in the DataFrame and append it to a list of dataframes
                    filter_and_move_to_list_of_df(current_records, df_list)
                else:
                    parsing_current_asset_category = True
                
                headers = {}
                current_records = []
                headers = fields # Store the current section's header

            elif row_type.lower() == "data":
                save_current_row()
        
        # Process the last section, because there is no futher headers to trigger the process
        if parsing_current_asset_category:
            filter_and_move_to_list_of_df(current_records, df_list)

        # Concatenate all DataFrames in the list
        combined_df = pd.concat(df_list, ignore_index=True)

    return combined_df


# def convert_to_dataframe(records_dict):
#     # Convert each section’s list of dictionaries into its own DataFrame
#     df = {}
#     for title, records in records_dict.items():
#         # section is the dictionary key
#         # records_list is the list of row dictionaries
#         df = pd.DataFrame(records_list)
#         # Rename some of the value headers to Amount so they are similar with all other dataframes
#         df.rename(columns=RENAME_DICT, inplace=True)
#         section_dataframes[section] = df

#     return section_dataframes

'''
1. Parse a section into a dataframe
2. Filter the DataFrame to hold only pre-agreed columns
3. Append the filtered DataFrame to a list of DataFrames
4. Combine the list of DataFrames into a new and clean DataFrame 
'''