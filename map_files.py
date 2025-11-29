#!/usr/bin/env python3
"""
File Mapper Script
Maps corresponding lines from two input files and creates a mapping output file.
The second file will be processed with text splitting using the specified max_length.

Usage: python map_files.py <input1> <input2> <output> [max_length]
"""

import sys
import os
from split_text import split_string

def map_files(input1_path, input2_path, output_path, max_length):
    """
    Read two input files and create a mapping file.
    
    Args:
        input1_path: Path to first input file
        input2_path: Path to second input file  
        output_path: Path to output mapping file
        max_length: Maximum length for text splitting
    """
    try:
        # Read both input files
        with open(input1_path, 'r', encoding='utf-8') as f1:
            lines1 = f1.readlines()
        
        with open(input2_path, 'r', encoding='utf-8') as f2:
            lines2 = f2.readlines()
        
        # Check if files have the same number of lines
        if len(lines1) != len(lines2):
            print(f"Warning: Files have different number of lines!")
            print(f"File 1: {len(lines1)} lines")
            print(f"File 2: {len(lines2)} lines")
            print("Proceeding with minimum number of lines...")
        
        # Use the minimum number of lines
        min_lines = min(len(lines1), len(lines2))
        
        # Create the mapping file
        with open(output_path, 'w', encoding='utf-8') as output_file:
            for i in range(min_lines):
                line1 = lines1[i].rstrip('\n\r')  # Remove newlines but keep content
                line2 = lines2[i].rstrip('\n\r')  # Remove newlines but keep content
                
                # Skip lines that start with ###IGNORE### in the Hebrew file
                if line2.startswith('###IGNORE###'):
                    continue
                
                # Handle empty lines - if both lines are empty, write empty line
                if not line1.strip() and not line2.strip():
                    output_file.write("\n")
                else:
                    # Handle cases where only one line is empty
                    if not line1.strip():
                        line1 = ""
                    if not line2.strip():
                        line2 = ""
                    
                    # Write the mapping
                    if "500" in output_path and not "5000" in output_path:
                        #line2 = split_string(line2, 100000, False)
                        line2 = split_string(line2, 22, False)
                    else:
                        line2 = split_string(line2, max_length, False)
                    output_file.write(f"{line1} === {line2}\n")
        
        print(f"Mapping file created successfully: {output_path}")
        print(f"Processed {min_lines} lines")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find input file - {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"Error: Permission denied - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) not in [4, 5]:
        print("Usage: python map_files.py <input1> <input2> <output> [max_length]")
        print()
        print("Arguments:")
        print("  input1     - Path to first input text file")
        print("  input2     - Path to second input text file")
        print("  output     - Path to output mapping file")
        print("  max_length - Maximum length for text splitting (default: 29)")
        print()
        print("Examples:")
        print("  python map_files.py english.txt hebrew.txt mapping.txt")
        print("  python map_files.py english.txt hebrew.txt mapping.txt 35")
        sys.exit(1)
    
    input1_path = sys.argv[1]
    input2_path = sys.argv[2]
    output_path = sys.argv[3]
    
    # Parse max_length argument or use default
    if len(sys.argv) == 5:
        try:
            max_length = int(sys.argv[4])
        except ValueError:
            print("Error: max_length must be a valid integer")
            print("Usage: python map_files.py <input1> <input2> <output> [max_length]")
            sys.exit(1)
    else:
        max_length = 29  # Default value
    
    # Validate input files exist
    if not os.path.exists(input1_path):
        print(f"Error: Input file 1 does not exist: {input1_path}")
        sys.exit(1)
    
    if not os.path.exists(input2_path):
        print(f"Error: Input file 2 does not exist: {input2_path}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    print(f"Input file 1: {input1_path}")
    print(f"Input file 2: {input2_path}")
    print(f"Output file: {output_path}")
    print(f"Max length: {max_length}")
    print()
    
    map_files(input1_path, input2_path, output_path, max_length)

if __name__ == "__main__":
    main()