#!/usr/bin/env python3
"""
Extract BMP file from PBM (PBMP) file format.

PBM File Structure (all bytes in little endian):
- 4 bytes: "PBMP" signature
- 4 bytes: ignore
- 4 bytes: "head" signature
- 4 bytes: number of chunks
- 4 bytes: version
- 4 bytes: width
- 4 bytes: height
- 4 bytes: bit count
- 4 bytes: flags
- 4 bytes: "data" signature
- 4 bytes: size (height × width)
- (height × width) bytes: BMP file data
- remaining bytes: ignorable

Usage: python extract_bmp_from_pbm.py <input_pbm_file> <output_bmp_file>
"""

import sys
import struct
import os
from PIL import Image


def read_string(file, length):
    """Read a fixed-length string from file."""
    return file.read(length).decode('ascii', errors='ignore')


def read_uint32(file):
    """Read a 4-byte unsigned integer (little endian)."""
    return struct.unpack('<I', file.read(4))[0]


def extract_bmp_from_pbm(input_path, output_path):
    """
    Extract BMP file data from PBM file.
    
    Args:
        input_path: Path to input PBM file
        output_path: Path to output BMP file
    """
    try:
        with open(input_path, 'rb') as pbm_file:
            # Read and verify "PBMP" signature
            signature = read_string(pbm_file, 4)
            if signature != "PBMP":
                print(f"Error: Invalid PBM file signature. Expected 'PBMP', got '{signature}'")
                return False
            print(f"✓ Valid PBM signature: {signature}")
            
            # Skip 4 bytes (ignore)
            pbm_file.read(4)
            
            # Read and verify "head" signature
            head_signature = read_string(pbm_file, 4)
            if head_signature != "head":
                print(f"Error: Invalid head signature. Expected 'head', got '{head_signature}'")
                return False
            print(f"✓ Valid head signature: {head_signature}")
            
            # Read header information
            num_chunks = read_uint32(pbm_file)
            version = read_uint32(pbm_file)
            width = read_uint32(pbm_file)
            height = read_uint32(pbm_file)
            bit_count = read_uint32(pbm_file)
            flags = read_uint32(pbm_file)
            
            print(f"\nPBM Header Information:")
            print(f"  Number of chunks: {num_chunks}")
            print(f"  Version: {version}")
            print(f"  Width: {width}")
            print(f"  Height: {height}")
            print(f"  Bit count: {bit_count}")
            print(f"  Flags: {flags}")
            
            # Read and verify "data" signature
            data_signature = read_string(pbm_file, 4)
            if data_signature != "data":
                print(f"Error: Invalid data signature. Expected 'data', got '{data_signature}'")
                return False
            print(f"✓ Valid data signature: {data_signature}")
            
            # Read data size
            data_size = read_uint32(pbm_file)
            expected_size = height * width
            print(f"\nData size: {data_size} bytes")
            print(f"Expected size (height × width): {expected_size} bytes")
            
            if data_size != expected_size:
                print(f"Warning: Data size mismatch! Using the value from header: {data_size}")
            
            # Read BMP data
            bmp_data = pbm_file.read(data_size)
            
            if len(bmp_data) != data_size:
                print(f"Error: Could not read expected amount of data.")
                print(f"Expected: {data_size} bytes, Got: {len(bmp_data)} bytes")
                return False
            
            print(f"✓ Successfully read {len(bmp_data)} bytes of BMP data")
            
            # Create PIL Image from bitmap data (8-bit grayscale) and save as BMP
            if len(bmp_data) == data_size and width > 0 and height > 0:
                # Create PIL Image from bitmap data (8-bit grayscale)
                img = Image.new('L', (width, height))
                img.putdata(bmp_data)
                
                # Save as BMP
                img.save(output_path)
                print(f"\n✓ BMP file extracted successfully: {output_path}")
                print(f"  Output file size: {len(bmp_data)} bytes")
            else:
                print(f"Error: Invalid dimensions or data size")
                return False
            
            return True
            
    except FileNotFoundError:
        print(f"Error: Could not find input file: {input_path}")
        return False
    except PermissionError as e:
        print(f"Error: Permission denied - {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) != 3:
        print("Extract BMP file from PBM (BPMP) format")
        print()
        print("Usage: python extract_bmp_from_pbm.py <input_pbm_file> <output_bmp_file>")
        print()
        print("Arguments:")
        print("  input_pbm_file  - Path to input PBM file")
        print("  output_bmp_file - Path to output BMP file")
        print()
        print("Example:")
        print("  python extract_bmp_from_pbm.py input.pbm output.bmp")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Validate input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file does not exist: {input_path}")
        sys.exit(1)
    
    # Create output directory if needed
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    print(f"Input PBM file: {input_path}")
    print(f"Output BMP file: {output_path}")
    print()
    
    # Extract BMP
    success = extract_bmp_from_pbm(input_path, output_path)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
