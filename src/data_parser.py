# Handles CSV file parsing

import os
import pandas as pd
import csv
from collections import defaultdict

from src.calculations import get_file_path
from src.data_selection import REQUIRED_SECTIONS


def parse_data(data):
    # Parse the content into sections and filter only required ones
    filtered_sections = defaultdict(list) # Initialize dictionary to store data
    section_headers = {} # Initialize dictionary to store headers
    instrument_information_list = []
    for line in data:
        # parts = [part.strip() for part in line.strip().split(',')]
        if line:
            section_name = line[0]
            if section_name in REQUIRED_SECTIONS:
                if line[1].lower() == 'header':
                    section_headers[section_name] = line[2:] # Store the header row
                else:
                    filtered_sections[section_name].append(line[2:]) # Append data rows to the filtered sections

            elif section_name == 'Financial Instrument Information':
                instrument_information_list.append(line[1:])
    
def load_csv(filename):
    file_path = get_file_path(filename, 'data', 'raw')
    print(f"🔍 Looking for file at: {file_path}")  # DEBUG OUTPUT
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")  # Show full path in error
    
    # Load the file as raw text to examine its structure
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = []
        max_length = 0

        for row in reader:
            data.append(row)
            max_length = max(max_length, len(row))  # Track the longest row length
    
    return parse_data(data)
