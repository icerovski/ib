import sys
import os
import pandas as pd

# Ensure the 'src' folder is in the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.calculations import get_file_path, summarize_section
from src.data_parser import parse_data, convert_to_dataframe
from src.streamlit_viewer import display_df
from src.storage import write_to_excel

def main():
    # month_input = input('Provide YYYYMM:')
    # ib_file_name = 'U16432685' + '_' + month_input + '_' + month_input + ".csv"
    ib_file_name = 'U16432685_202501_202501.csv'
    file_path = get_file_path(ib_file_name, 'data', 'raw')

    parsed_data = parse_data(file_path)
    sections_df = convert_to_dataframe(parsed_data)

    pnl = {}
    result = None
    for k, v in sections_df.items():
        # display_df(k, v)
        result = pd.to_numeric(v.iloc[-1]['Amount'], errors='coerce')
        pnl[k] = result
    
    # Convert dictionary to DataFrame with keys as index
    pnl_df = pd.DataFrame.from_dict(pnl, orient="index", columns=["Amount"])

    # Add a total row at the bottom
    pnl_df.loc["Total"] = pnl_df["Amount"].sum()

    display_df('Amount', pnl_df)
    write_to_excel(pnl_df, ib_file_name)
    
if __name__ == "__main__":
    main()