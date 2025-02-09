# Handles saving results to CSV or database
import pandas as pd

from src.calculations import get_file_path, remove_csv_extension, sanitize_sheet_name
from src.data_selection import pnl_mapping

def write_to_excel(dataframes, filename):
    """
    Writes a dictionary of DataFrames to an Excel file with multiple sheets.

    Args:
        dataframes (dict): Dictionary where keys are section names and values are Pandas DataFrames.
        output_file (str): Path to the output Excel file.
    """

    output_file_path = remove_csv_extension(get_file_path(filename, "data", "raw"))
    output_file = output_file_path + "_parsed" + ".xlsx"

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for section, df in dataframes.items():
            # sheet_name = section[:31]  # Excel sheet names are limited to 31 characters
            sheet_name = sanitize_sheet_name(section)
            df.to_excel(writer, sheet_name=sheet_name, index=True)
    
    print(f"Excel file '{output_file}' has been created.")

def filter_sections(df_dict):
    # pnl_mapping.values() contains lists, and I want to iterate over the values inside those lists 
    # to use them as keys in filtered_dict
    filtered_dict = {item: 0 for sublist in pnl_mapping.values() for item in sublist}

    # for k, v in filtered_dict.items():
    #     if k in df_dict.keys():
    #         filtered_dict[k] = df_dict[k]
    
    for k, v in df_dict.items():
        if k in filtered_dict.keys():
            filtered_dict[k] = v

    return filtered_dict


def build_pnl(df_dict):
    # Initialize dictionary to store extracted values
    pnl_values = {component: 0 for component in pnl_mapping.keys()}

    # Iterate through the PNL components and sum relevant sections
    for component, section_names in pnl_mapping.items():
        current_amount = 0
        section_amount = 0

        for section in section_names:
            if section in df_dict:
                current_df = df_dict[section]
                current_amount = pd.to_numeric(current_df.iloc[-1]['Amount'], errors='coerce')
                section_amount += current_amount
        pnl_values[component] = section_amount
    
    # Convert to a DataFrame
    pnl_df = pd.DataFrame.from_dict(pnl_values, orient="index", columns=["Amount"])

    # Add a total row at the bottom
    pnl_df.loc["Total"] = pnl_df["Amount"].sum()
    
    return pnl_df

