import pandas as pd

# Define mapping of PNL components to actual sections in the parsed DataFrame dictionary
PNL_MAPPING = {
    'Trading Profit': ['Realized & Unrealized Performance Summary'],
    'Net Dividend Income': ['Dividends', 'Withholding Tax'],
    'Net Interest Profit': ['Bond Interest Received', 'Bond Interest Paid', 'Broker Interest Received', 'Broker Interest Paid'],
    'OpEx': ["Other Fees", "Sales Tax Details"],
}

def filter_sections(df_dict):
    # pnl_mapping.values() contains lists, and I want to iterate over the values inside those lists 
    # to use them as keys in filtered_dict
    filtered_dict = {item: 0 for sublist in PNL_MAPPING.values() for item in sublist}
    
    for k, v in df_dict.items():
        if k in filtered_dict.keys():
            filtered_dict[k] = v

    return filtered_dict

def build_pnl(df_dict):
    # Initialize dictionary to store extracted values
    pnl_values = {component: 0 for component in PNL_MAPPING.keys()}

    # Iterate through the PNL components and sum relevant sections
    for component, section_names in PNL_MAPPING.items():
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