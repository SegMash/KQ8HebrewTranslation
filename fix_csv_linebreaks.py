"""
Fix CSV files that have line breaks within quoted text fields.
This script merges lines that are part of a single CSV record back together.
"""

import argparse
import csv
import re


def fix_csv_linebreaks(input_file, output_file=None):
    """
    Fix CSV file by merging lines that are broken within quoted text fields.
    
    Args:
        input_file: Path to the input CSV file
        output_file: Path to the output CSV file (defaults to input_file if not specified)
    """
    if output_file is None:
        output_file = input_file
    
    # Read the entire file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i].rstrip('\n')
        
        # Check if this is a header line or a properly formatted CSV line
        # A valid CSV line should have 10 commas (11 fields) and if it has quotes,
        # they should be balanced
        if i == 0 or is_complete_csv_line(line):
            fixed_lines.append(line)
            i += 1
        else:
            # This line is incomplete, merge with following lines
            merged_line = line
            i += 1
            
            # Keep merging until we have a complete CSV record
            while i < len(lines):
                next_line = lines[i].rstrip('\n')
                
                # Replace the newline with a space when merging
                merged_line += ' ' + next_line
                i += 1
                
                # Check if we now have a complete record
                if is_complete_csv_line(merged_line):
                    break
            
            fixed_lines.append(merged_line)
    
    # Write the fixed content
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        for line in fixed_lines:
            f.write(line + '\n')
    
    print(f"Fixed CSV written to: {output_file}")
    print(f"Original lines: {len(lines)}")
    print(f"Fixed lines: {len(fixed_lines)}")
    print(f"Lines merged: {len(lines) - len(fixed_lines)}")


def is_complete_csv_line(line):
    """
    Check if a line represents a complete CSV record.
    A complete line should have:
    - 10 commas (11 fields total)
    - Balanced quotes (even number of quotes, or quotes properly closed)
    """
    # Count commas outside of quoted strings
    in_quote = False
    comma_count = 0
    quote_count = 0
    
    for char in line:
        if char == '"':
            quote_count += 1
            in_quote = not in_quote
        elif char == ',' and not in_quote:
            comma_count += 1
    
    # A complete CSV line should have:
    # 1. Exactly 10 commas (for 11 fields)
    # 2. Even number of quotes (all quotes are balanced)
    # 3. Not currently inside a quote
    return comma_count == 10 and quote_count % 2 == 0 and not in_quote


def main():
    parser = argparse.ArgumentParser(
        description='Fix CSV files that have line breaks within quoted text fields'
    )
    parser.add_argument('input_file', help='Path to the input CSV file')
    parser.add_argument('-o', '--output', dest='output_file',
                        help='Path to the output CSV file (default: overwrite input file)')
    
    args = parser.parse_args()
    
    fix_csv_linebreaks(args.input_file, args.output_file)


if __name__ == '__main__':
    main()
