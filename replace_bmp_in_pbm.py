#!/usr/bin/env python3
"""
Replace BMP data inside a PBM (PBMP) file.
Assumes the BMP size hasn't changed - only the content.

Usage: python replace_bmp_in_pbm.py <pbm_file> <bmp_file>
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


def replace_bmp_in_pbm(pbm_path, bmp_path):
    """
    Replace BMP data inside a PBM file.
    
    Args:
        pbm_path: Path to PBM file to modify
        bmp_path: Path to BMP file with new data
    """
    try:
        # Load the BMP file using PIL
        img = Image.open(bmp_path)
        
        # Convert to 8-bit grayscale if not already
        if img.mode != 'L':
            img = img.convert('L')
        
        # Get BMP dimensions and pixel data
        bmp_width, bmp_height = img.size
        bmp_data = list(img.getdata())
        bmp_bytes = bytes(bmp_data)
        
        print(f"BMP File Information:")
        print(f"  Width: {bmp_width}")
        print(f"  Height: {bmp_height}")
        print(f"  Data size: {len(bmp_bytes)} bytes")
        print()
        
        # Read the PBM file
        with open(pbm_path, 'rb') as pbm_file:
            # Read and verify "PBMP" signature
            signature = read_string(pbm_file, 4)
            if signature != "PBMP":
                print(f"Error: Invalid PBM file signature. Expected 'PBMP', got '{signature}'")
                return False
            
            # Skip 4 bytes (ignore)
            pbm_file.read(4)
            
            # Read and verify "head" signature
            head_signature = read_string(pbm_file, 4)
            if head_signature != "head":
                print(f"Error: Invalid head signature. Expected 'head', got '{head_signature}'")
                return False
            
            # Read header information
            num_chunks = read_uint32(pbm_file)
            version = read_uint32(pbm_file)
            pbm_width = read_uint32(pbm_file)
            pbm_height = read_uint32(pbm_file)
            bit_count = read_uint32(pbm_file)
            flags = read_uint32(pbm_file)
            
            print(f"PBM Header Information:")
            print(f"  Width: {pbm_width}")
            print(f"  Height: {pbm_height}")
            print(f"  Bit count: {bit_count}")
            print()
            
            # Verify dimensions match
            if bmp_width != pbm_width or bmp_height != pbm_height:
                print(f"Error: Dimension mismatch!")
                print(f"  PBM: {pbm_width}x{pbm_height}")
                print(f"  BMP: {bmp_width}x{bmp_height}")
                return False
            
            # Read and verify "data" signature
            data_signature = read_string(pbm_file, 4)
            if data_signature != "data":
                print(f"Error: Invalid data signature. Expected 'data', got '{data_signature}'")
                return False
            
            # Read data size
            data_size = read_uint32(pbm_file)
            expected_size = pbm_height * pbm_width
            
            if len(bmp_bytes) != data_size:
                print(f"Error: BMP data size doesn't match PBM data size!")
                print(f"  PBM expects: {data_size} bytes")
                print(f"  BMP provides: {len(bmp_bytes)} bytes")
                return False
            
            # Remember position where BMP data starts
            bmp_data_offset = pbm_file.tell()
            
            # Skip the old BMP data
            pbm_file.read(data_size)
            
            # Read remaining bytes after BMP data (if any)
            remaining_data = pbm_file.read()
        
        # Now write the modified PBM file
        with open(pbm_path, 'rb') as pbm_file:
            # Read everything up to the BMP data
            header_data = pbm_file.read(bmp_data_offset)
        
        # Write the complete file with new BMP data
        with open(pbm_path, 'wb') as pbm_file:
            # Write header (everything before BMP data)
            pbm_file.write(header_data)
            
            # Write new BMP data
            pbm_file.write(bmp_bytes)
            
            # Write remaining data (if any)
            if remaining_data:
                pbm_file.write(remaining_data)
        
        print(f"✓ Successfully replaced BMP data in PBM file: {pbm_path}")
        print(f"  Replaced {len(bmp_bytes)} bytes of BMP data")
        
        return True
        
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
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
        print("Replace BMP data inside PBM (PBMP) file")
        print()
        print("Usage: python replace_bmp_in_pbm.py <pbm_file> <bmp_file>")
        print()
        print("Arguments:")
        print("  pbm_file - Path to PBM file to modify")
        print("  bmp_file - Path to BMP file with new data")
        print()
        print("Note: The BMP dimensions must match the original dimensions in the PBM file.")
        print()
        print("Example:")
        print("  python replace_bmp_in_pbm.py main18.pbm main18_modified.bmp")
        sys.exit(1)
    
    pbm_path = sys.argv[1]
    bmp_path = sys.argv[2]
    
    # Validate files exist
    if not os.path.exists(pbm_path):
        print(f"Error: PBM file does not exist: {pbm_path}")
        sys.exit(1)
    
    if not os.path.exists(bmp_path):
        print(f"Error: BMP file does not exist: {bmp_path}")
        sys.exit(1)
    
    print(f"PBM file: {pbm_path}")
    print(f"BMP file: {bmp_path}")
    print()
    
    # Replace BMP data
    success = replace_bmp_in_pbm(pbm_path, bmp_path)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
