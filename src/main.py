import sys
import os
import streamlit as st

# Ensure the 'src' folder is in the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.calculations import get_file_path
from src.data_parser import parse_data, convert_to_dataframe
from src.streamlit_viewer import display_df, display_sections
from src.storage import write_to_excel
from src.instruments_info import parse_info_section
from src.pnl import build_pnl, filter_sections
from src.pnl_parser import pnl_parser

def main():
    # month_input = input('Provide YYYYMM:')
    # ib_file_name = 'U16432685' + '_' + month_input + '_' + month_input + ".csv"
    ib_file_name = 'U16432685_202501_202501.csv'
    file_path = get_file_path(ib_file_name, 'data', 'raw')

    parsed_data = parse_data(file_path)
    sections_df = convert_to_dataframe(parsed_data)

    instruments_info = parse_info_section(file_path) # Financial Instruments Information
    filtered_df = filter_sections(sections_df) # summary of all sections that are included in the P&L calculation

    # st.set_page_config(layout="wide") # Enable wide mode for full monitor coverage
    display_df("Financial Instruments Information", instruments_info)
    display_sections(filtered_df)

    # Profit & Loss statement
    pnl_df = pnl_parser(file_path)
    display_df('Profit & Loss', pnl_df)

    # pnl_df = build_pnl(sections_df)
    # display_df('Profit & Loss', pnl_df)
    # write_to_excel(pnl_df, ib_file_name)
    
if __name__ == "__main__":
    main()