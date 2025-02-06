# Handles saving results to CSV or database
import pandas as pd
import re

from src.calculations import get_file_path, remove_csv_extension

def sanitize_sheet_name(raw_name, max_len=31):
    # Replace invalid Excel characters with underscores:
    safe_name = re.sub(r"[/\\\?\*\[\]:]", "_", raw_name)
    # Truncate to 31 characters (Excel’s limit)
    return safe_name[:max_len]

def save_to_excel(parsed_sections, filename):
    filename = remove_csv_extension(filename)
    parsed_file_path = get_file_path(filename, "data", "parsed") + "_parsed" + ".xlsx"
    # Build output Excel filename with same base name
    # base, _ = os.path.splitext(filename)
    excel_file = parsed_file_path + "_parsed" + ".xlsx"
    # file_path = get_file_path(excel_file)

    with pd.ExcelWriter(parsed_file_path, engine='openpyxl') as writer:
        for section_name, df_list in parsed_sections.items():
            for i, df in enumerate(df_list, start=1):
                # Excel worksheet names have a 31-char limit; trim if needed
                sheet_name = f"{section_name}_{i}"
                sheet_name = sanitize_sheet_name(sheet_name)

                df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"Done.  Saved parsed sections to {parsed_file_path}")