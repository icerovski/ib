import sys
import os
import pandas as pd

# Ensure the 'src' folder is in the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.calculations import get_file_path, summarize_section
from src.data_parser import parse_data, convert_to_dataframe
from src.streamlit_viewer import display_df
from src.storage import write_to_excel
from src.data_selection import pnl_mapping

def main():
    # month_input = input('Provide YYYYMM:')
    # ib_file_name = 'U16432685' + '_' + month_input + '_' + month_input + ".csv"
    ib_file_name = 'U16432685_202501_202501.csv'
    file_path = get_file_path(ib_file_name, 'data', 'raw')

    parsed_data = parse_data(file_path)
    sections_df = convert_to_dataframe(parsed_data)

    # Initialize dictionary to store extracted values
    pnl_values = {component: 0 for component in pnl_mapping.keys()}

    # Iterate through the PNL components and sum relevant sections
    for component, section_names in pnl_mapping.items():
        current_amount = 0
        section_amount = 0

        for section in section_names:
            if section in sections_df:
                current_df = sections_df[section]
                current_amount = pd.to_numeric(current_df.iloc[-1]['Amount'], errors='coerce')
                section_amount += current_amount
        pnl_values[component] = section_amount
    
    # Convert to a DataFrame
    pnl_df = pd.DataFrame.from_dict(pnl_values, orient="index", columns=["Amount"])

    # Add a total row at the bottom
    pnl_df.loc["Total"] = pnl_df["Amount"].sum()

    display_df('P&L', pnl_df)
    write_to_excel(pnl_df, ib_file_name)
    
if __name__ == "__main__":
    main()