#!/usr/bin/env python3
"""
Script to create a CSV file from English and Hebrew translation files.
Takes 3 arguments: english_file, hebrew_file, target_csv_file
"""

import csv
import sys
import os


def read_lines(file_path):
    """Read all lines from a file, handling encoding."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.rstrip('\n\r') for line in f]
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            return [line.rstrip('\n\r') for line in f]


def create_csv(english_file, hebrew_file, target_csv):
    """
    Read English and Hebrew files and create a CSV with 4 columns:
    english, hebrew, tested?, comments
    """
    # Read both files
    english_lines = read_lines(english_file)
    hebrew_lines = read_lines(hebrew_file)
    
    # Get the maximum length to handle files of different sizes
    max_lines = max(len(english_lines), len(hebrew_lines))
    
    # Create CSV file
    rows_written = 0
    with open(target_csv, 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        #writer.writerow(['english', 'hebrew', 'tested?', 'comments'])
        
        # Write data rows, skipping empty sentences
        for i in range(max_lines):
            english = english_lines[i] if i < len(english_lines) else ''
            hebrew = hebrew_lines[i] if i < len(hebrew_lines) else ''
            
            # Skip rows where both english and hebrew are empty (after stripping whitespace)
            if english.strip() == '' and hebrew.strip() == '':
                continue
            
            # Write row with empty tested? and comments columns
            writer.writerow([english, hebrew, '', ''])
            rows_written += 1
    
    print(f"CSV file created successfully: {target_csv}")
    print(f"Total rows written: {rows_written} (skipped {max_lines - rows_written} empty lines)")


def main():
    if len(sys.argv) != 4:
        print("Usage: python create_csv.py <english_file> <hebrew_file> <target_csv_file>")
        sys.exit(1)
    
    english_file = sys.argv[1]
    hebrew_file = sys.argv[2]
    target_csv = sys.argv[3]
    
    # Check if input files exist
    if not os.path.exists(english_file):
        print(f"Error: English file not found: {english_file}")
        sys.exit(1)
    
    if not os.path.exists(hebrew_file):
        print(f"Error: Hebrew file not found: {hebrew_file}")
        sys.exit(1)
    
    # Create the CSV file
    create_csv(english_file, hebrew_file, target_csv)


if __name__ == "__main__":
    main()

