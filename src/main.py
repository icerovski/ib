import sys
import os
import pandas as pd

# Ensure the 'src' folder is in the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.calculations import get_file_path
from src.data_parser import parse_data, convert_to_dataframe
from src.streamlit_viewer import display_df
from src.storage import write_to_excel, build_pnl, filter_sections

def main():
    # month_input = input('Provide YYYYMM:')
    # ib_file_name = 'U16432685' + '_' + month_input + '_' + month_input + ".csv"
    ib_file_name = 'U16432685_202501_202501.csv'
    file_path = get_file_path(ib_file_name, 'data', 'raw')

    parsed_data = parse_data(file_path)
    sections_df = convert_to_dataframe(parsed_data)

    filtered_df = filter_sections(sections_df)
    for k, v in filtered_df.items():
        display_df(k, v)

    pnl_df = build_pnl(sections_df)   
    display_df('P&L', pnl_df)
    write_to_excel(pnl_df, ib_file_name)
    
if __name__ == "__main__":
    main()