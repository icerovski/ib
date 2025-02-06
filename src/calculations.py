import os

def get_file_path(filename, *args):
    """Returns the absolute path of a file inside 'data/raw', or any other directory provided in *args."""
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
    data_dir = os.path.abspath(os.path.join(current_dir, "..", *args))  # Navigate to 'data/raw'
    file_path = os.path.join(data_dir, filename)  # Combine with filename

    return file_path

def remove_csv_extension(file_path):
    """Removes the .csv extension from a file path."""
    file_without_ext, _ = os.path.splitext(file_path)
    return file_without_ext