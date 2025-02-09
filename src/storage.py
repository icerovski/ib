# Handles saving results to CSV or database
import pandas as pd

from src.calculations import get_file_path, remove_csv_extension, sanitize_sheet_name

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


