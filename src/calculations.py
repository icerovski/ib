import os

def remove_csv_extension(file_path):
    """Removes the .csv extension from a file path."""
    file_without_ext, _ = os.path.splitext(file_path)
    return file_without_ext

def print_dict_pretty(d, indent=0):
    # Hint: Loop through items, handle nested dictionaries recursively
    # The 'indent' value is used to create spaces for readability
    for key, value in d.items():
        if isinstance(value, list) and all(isinstance(item, list) for item in value):
        # # Hint: If value is a list of lists, print each sub-list separately
        # # Hint: Use string multiplication to control indentation
            print(" " * indent + str(key) + ": ")
            for sub_list in value:
                # Hint: Print each sub_list on a new line, 
                # you can add indentation if you want
                print(" ", sub_list)
        # if isinstance(value, dict):
        #     print_dict_pretty(value, indent + 4)  # recursively call for nested dictionaries
        else:
            # Hint: Print value with extra indentation
            print(" " * (indent + 4) + str(value))


def get_file_path(filename, *args):
    """Returns the absolute path of a file inside 'data/raw', or any other directory provided in *args."""
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
    data_dir = os.path.abspath(os.path.join(current_dir, "..", *args))  # Navigate to 'data/raw'
    file_path = os.path.join(data_dir, filename)  # Combine with filename
    print(f"🔍 Looking for file at: {file_path}")  # DEBUG OUTPUT
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")  # Show full path in error
    
    return file_path