#!/usr/bin/env python3
"""
PPL (KQ8 Palette) Parser
Parses King's Quest 8 palette files (.ppl) and converts them to JASC-PAL format

Based on documentation from: https://svn.nicode.net/libkq8fpc/doc/kq8ppal.txt
"""

import struct
import sys
import os

def parse_ppl_file(filename, output_filename=None):
    """
    Parse a KQ8 PPL palette file and extract palette data
    
    Args:
        filename: Path to the .ppl file
        output_filename: Path to output .pal file (optional)
    """
    
    print(f"Parsing PPL file: {filename}")
    print("=" * 60)
    
    # Default system palette colors (first 8 and last 8)
    pal_first = [
        (0x00, 0x00, 0x00), (0x80, 0x00, 0x00), (0x00, 0x80, 0x00),
        (0x80, 0x80, 0x00), (0x00, 0x00, 0x80), (0x80, 0x00, 0x80),
        (0x00, 0x80, 0x80), (0xC0, 0xC0, 0xC0)
    ]
    
    pal_last = [
        (0x80, 0x80, 0x80), (0xFF, 0x00, 0x00), (0x00, 0xFF, 0x00),
        (0xFF, 0xFF, 0x00), (0x00, 0x00, 0xFF), (0xFF, 0x00, 0xFF),
        (0x00, 0xFF, 0xFF), (0xFF, 0xFF, 0xFF)
    ]
    
    palette_colors = [(0, 0, 0)] * 256  # Initialize with black
    
    # Set default system colors
    for i, color in enumerate(pal_first):
        palette_colors[i] = color
    for i, color in enumerate(pal_last):
        palette_colors[248 + i] = color
    
    with open(filename, 'rb') as f:
        file_size = os.path.getsize(filename)
        print(f"File size: {file_size} bytes")
        
        # Check if it's a RIFF palette first
        f.read(4) #"PPAL"
        f.read(4) #"F$..""
        f.read(4) #"head"
        f.read(4) #chunk count
        f.read(4) #version
        f.read(4) #"data"
        
        print("  Reading palette data (256 colors)")
        # Read 256 PALETTEENTRY structures (4 bytes each: R G B flags)
        for i in range(256):
            r, g, b, flags = struct.unpack('BBBB', f.read(4))
            palette_colors[i] = (r, g, b)
            #print(f"    Color {i:3d}: ({r:3d},{g:3d},{b:3d}) flags=0x{flags:02X}")
        
        f.tell()
        # Read the rest of the file for any additional data
        rest_of_file = f.read()
        if rest_of_file:
            print(f"  Found additional data after palette: {len(rest_of_file)} bytes")

    # Generate output PAL file
    if output_filename is None:
        output_filename = os.path.splitext(filename)[0] + '.pal'
    
    print(f"\nGenerating JASC-PAL file: {output_filename}")
    
    with open(output_filename, 'w') as f:
        f.write('JASC-PAL\n')
        f.write('0100\n')
        f.write('256\n')
        
        for r, g, b in palette_colors:
            f.write(f'{r} {g} {b}\n')
    
    print(f"Successfully created palette file: {output_filename}")
    print(f"Palette contains 256 colors")
    
    # Show some sample colors
    #print("\nSample colors:")
    #for i in [0, 1, 16, 32, 64, 128, 200, 248, 255]:
    #    r, g, b = palette_colors[i]
    #    print(f"  Color {i:3d}: R={r:3d} G={g:3d} B={b:3d}")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("PPL (KQ8 Palette) Parser")
        print("=" * 30)
        print("")
        print("Usage:")
        print("  python parse_ppl.py <ppl_file> [output_pal_file]")
        print("")
        print("Examples:")
        print("  python parse_ppl.py game.ppl")
        print("  python parse_ppl.py game.ppl game_palette.pal")
        print("")
        print("The script will:")
        print("  - Parse all chunks in the PPL file")
        print("  - Extract the 256-color palette from 'data' chunk")
        print("  - Print all uint8_t variables found")
        print("  - Generate a JASC-PAL format file")
        return
    
    ppl_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Check if file exists
    if not os.path.exists(ppl_file):
        print(f"Error: PPL file '{ppl_file}' not found")
        sys.exit(1)
    
    try:
        parse_ppl_file(ppl_file, output_file)
        
    except Exception as e:
        print(f"Error parsing PPL file: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()