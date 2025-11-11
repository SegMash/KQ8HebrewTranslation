import csv
import re
import argparse
import os

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Translate CSV messages using mapping file')
parser.add_argument('csv_file', help='Path to the input CSV file')
parser.add_argument('mapping_file', help='Path to the mapping file (English === Hebrew)')
parser.add_argument('output_file', help='Path to the output CSV file')
args = parser.parse_args()

# Validate input files exist
if not os.path.exists(args.csv_file):
    print(f"Error: Input CSV file '{args.csv_file}' not found.")
    exit(1)

if not os.path.exists(args.mapping_file):
    print(f"Error: Mapping file '{args.mapping_file}' not found.")
    exit(1)

# Function to remove all bracket sections from text
def remove_brackets(text):
    # Remove all patterns like ([...]), ([#]...), ([0]...), (TEXT), etc.
    pattern = r'\([^)]*\)'
    cleaned = re.sub(pattern, '', text)
    # Only strip leading/trailing whitespace, preserve original spacing
    cleaned = cleaned.strip()
    return cleaned

# Read and parse mapping file
print("Reading mapping file...")
mapping = {}
with open(args.mapping_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        if ' === ' in line:
            english, hebrew = line.split(' === ', 1)
            # Use the cleaned English text as key (remove brackets for matching)
            english_cleaned = remove_brackets(english)
            mapping[english_cleaned] = hebrew

print(f"Loaded {len(mapping)} translations from mapping file")

# Read the CSV file and convert to list of dictionaries
print("Reading CSV file...")
messages = []
with open(args.csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        # Convert numeric fields to integers for proper sorting
        row['noun'] = int(row['noun'])
        row['verb'] = int(row['verb'])
        row['case'] = int(row['case'])
        row['sequence'] = int(row['sequence'])
        messages.append(row)

# Sort by noun, then verb, then case, then sequence
messages.sort(key=lambda x: (x['noun'], x['verb'], x['case'], x['sequence']))

# Translate messages
print("Translating messages...")
translated_count = 0
not_found_count = 0

for msg in messages:
    original_text = msg['text']
    # Remove brackets from original text to match mapping
    cleaned_text = remove_brackets(original_text)
    
    # Look up Hebrew translation
    if cleaned_text in mapping:
        msg['text'] = mapping[cleaned_text]
        translated_count += 1
    else:
        # If not found, keep original or mark as missing
        print(f"Warning: Translation not found for: '{cleaned_text[:50]}...' original_text={original_text}")
        msg['text'] = cleaned_text  # Keep cleaned English text if no translation
        not_found_count += 1

# Write translated CSV file
print(f"Writing translated CSV to {args.output_file}...")
with open(args.output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for msg in messages:
        # Convert numeric fields back to strings for CSV
        row = msg.copy()
        row['noun'] = str(row['noun'])
        row['verb'] = str(row['verb'])
        row['case'] = str(row['case'])
        row['sequence'] = str(row['sequence'])
        writer.writerow(row)

print(f"\nTranslation complete!")
print(f"  Translated: {translated_count} messages")
print(f"  Not found: {not_found_count} messages")
print(f"  Total: {len(messages)} messages")
print(f"  Output written to: {args.output_file}")

