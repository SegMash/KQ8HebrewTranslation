#!/usr/bin/env python3
"""
Compare bytes at offset 0x242 between original and created font files
"""

def compare_bytes_at_offset(file1, file2, offset):
    """Compare bytes at specific offset between two files"""
    print(f"Comparing bytes at offset 0x{offset:X} ({offset})")
    print("=" * 50)
    
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        f1.seek(offset)
        f2.seek(offset)
        
        # Read 16 bytes around the target
        f1.seek(offset - 8)
        f2.seek(offset - 8)
        
        data1 = f1.read(16)
        data2 = f2.read(16)
        
        print(f"File 1 ({file1}):")
        hex1 = ' '.join(f'{b:02X}' for b in data1)
        print(f"  0x{offset-8:X}: {hex1}")
        print(f"                {'   ' * 8}^")
        
        print(f"File 2 ({file2}):")
        hex2 = ' '.join(f'{b:02X}' for b in data2)
        print(f"  0x{offset-8:X}: {hex2}")
        print(f"                {'   ' * 8}^")
        
        if data1[8] != data2[8]:  # byte at target offset
            print(f"\n*** DIFFERENCE at 0x{offset:X} ***")
            print(f"File 1: 0x{data1[8]:02X}")
            print(f"File 2: 0x{data2[8]:02X}")
        else:
            print(f"\nBytes match at 0x{offset:X}: 0x{data1[8]:02X}")

if __name__ == "__main__":
    original = "font/console.pft"
    created = "font/console_new.pft"
    offset = 0x242
    
    try:
        compare_bytes_at_offset(original, created, offset)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")