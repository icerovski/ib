import sys
import os

# Ensure the 'src' folder is in the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import parse_nonstandard_csv
from src.storage import save_to_excel

def main():
    # File path to the uploaded CSV
    month_input = input('Provide YYYYMM:')
    ib_file_name = 'U16432685' + '_' + month_input + '_' + month_input + ".csv"

    # Parse the raw file into a dictionary
    parsed_sections = parse_nonstandard_csv(ib_file_name)
    
    # Save the parsed data to an excel file
    save_to_excel(parsed_sections, ib_file_name) 
    
if __name__ == "__main__":
    main()