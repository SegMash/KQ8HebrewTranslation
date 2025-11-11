#!/usr/bin/env python3
"""
BMP to PNG Converter with Palette Support
Converts indexed BMP files to RGB PNG files using a palette file
"""

import sys
import os
import struct
from PIL import Image
import json

def load_palette_from_file(palette_file, debug=False):
    """
    Load palette data from a file. Supports multiple formats:
    - .pal files (JASC-PAL format or raw text)
    - .act files (Adobe Color Table)
    - .json files (custom JSON format)
    - .bin files (raw RGB data)
    """
    ext = os.path.splitext(palette_file)[1].lower()
    
    if ext == '.pal':
        # Try different .pal formats
        with open(palette_file, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines if line.strip()]  # Remove empty lines
            
            if len(lines) == 0:
                raise ValueError("Empty palette file")
            
            # Check for JASC-PAL format
            if lines[0] == 'JASC-PAL':
                if len(lines) < 3:
                    raise ValueError("Invalid JASC-PAL file: missing header")
                version = lines[1]
                color_count = int(lines[2])
                
                palette = []
                for i in range(3, min(3 + color_count, len(lines))):
                    try:
                        r, g, b = map(int, lines[i].split())
                        palette.extend([r, g, b])
                    except ValueError:
                        if debug:
                            print(f"Warning: Invalid color line {i}: '{lines[i]}'")
                        palette.extend([0, 0, 0])  # Default to black
                
                # Pad to 256 colors if needed
                while len(palette) < 768:  # 256 * 3
                    palette.extend([0, 0, 0])
                
                return palette
            
            else:
                # Try raw RGB text format (3 numbers per line or 3 columns)
                if debug:
                    print("Trying raw RGB text format...")
                palette = []
                
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 3:
                        try:
                            r, g, b = map(int, parts[:3])
                            palette.extend([r, g, b])
                        except ValueError:
                            if debug:
                                print(f"Warning: Invalid RGB line: '{line}'")
                            continue
                
                if len(palette) == 0:
                    raise ValueError("No valid RGB values found in palette file")
                
                # Pad to 256 colors if needed
                while len(palette) < 768:
                    palette.extend([0, 0, 0])
                
                if debug:
                    print(f"Loaded {len(palette)//3} colors from raw RGB format")
                return palette
    
    elif ext == '.act':
        # Adobe Color Table format (768 bytes = 256 colors × 3 RGB)
        with open(palette_file, 'rb') as f:
            palette_data = f.read(768)
            return list(palette_data)
    
    elif ext == '.json':
        # Custom JSON format: {"palette": [[r,g,b], [r,g,b], ...]}
        with open(palette_file, 'r') as f:
            data = json.load(f)
            palette = []
            for color in data['palette']:
                palette.extend(color[:3])  # Take only RGB, ignore alpha if present
            return palette
    
    elif ext == '.bin':
        # Raw binary RGB data
        with open(palette_file, 'rb') as f:
            palette_data = f.read()
            return list(palette_data)
    
    else:
        raise ValueError(f"Unsupported palette format: {ext}")

def create_default_grayscale_palette():
    """Create a default 256-color grayscale palette"""
    palette = []
    for i in range(256):
        palette.extend([i, i, i])  # R, G, B all the same for grayscale
    return palette

def extract_palette_from_font(font_file, debug=False):
    """
    Extract palette from KQ8 font file if it has one
    
    Args:
        font_file: Path to .pft font file
        debug: Whether to print debug information
        
    Returns:
        List of RGB values or None if no palette
    """
    try:
        with open(font_file, 'rb') as f:
            # Skip to the end to check for palette
            f.seek(-4, 2)  # Go to last 4 bytes
            has_palette = struct.unpack('<I', f.read(4))[0]
            
            if has_palette == 0:
                if debug:
                    print("Font file has no palette")
                return None
            
            if debug:
                print(f"Font file indicates palette present (value: {has_palette})")
            
            # For now, we'll return None since we need to implement
            # the actual palette reading logic
            if debug:
                print("Palette extraction from font files not yet implemented")
            return None
            
    except Exception as e:
        if debug:
            print(f"Error checking font palette: {e}")
        return None

def convert_bmp_to_png(bmp_file, output_file, palette=None, debug=False):
    """
    Convert indexed BMP file to RGB PNG using palette
    
    Args:
        bmp_file: Path to input BMP file
        output_file: Path to output PNG file  
        palette: List of RGB values [r1,g1,b1,r2,g2,b2,...] or None for grayscale
        debug: Whether to print debug information
    """
    # Load BMP file
    img = Image.open(bmp_file)
    
    if debug:
        print(f"Input image: {img.size[0]}x{img.size[1]}, mode: {img.mode}")
    
    # Convert to mode 'L' (8-bit grayscale) if not already
    #if img.mode != 'L':
    #    img = img.convert('L')
    
    # Get pixel data as indices
    
    width, height = img.size
    
    if palette is None:
        # Use default grayscale palette
        palette = create_default_grayscale_palette()
        if debug:
            print("Using default grayscale palette")
    else:
        if debug:
            print(f"Using custom palette with {len(palette)//3} colors")
    
    # Create palette mode image ('P')
    palette_img = Image.new('P', (width, height))
    
    # Set the palette data as bytes
    palette_bytes = bytes(palette[:768])  # Ensure exactly 768 bytes (256 colors * 3 RGB)
    palette_img.putpalette(palette_bytes)
    
    # Set the pixel data (indices remain as-is)
    palette_img.putdata(img.getdata())

    # Save as PNG with palette
    palette_img.save(output_file, 'PNG')
    if debug:
        print(f"Converted {bmp_file} -> {output_file} (palette mode)")

def convert_folder(input_folder, output_folder, palette_file=None, font_file=None, debug=False):
    """
    Convert all BMP files in a folder to PNG files
    
    Args:
        input_folder: Folder containing BMP files
        output_folder: Folder for output PNG files
        palette_file: Path to palette file (optional)
        font_file: Path to font file to extract palette from (optional)
        debug: Whether to print debug information
    """
    # Load palette if provided
    palette = None
    
    # Try to load palette from font file first
    if font_file and os.path.exists(font_file):
        try:
            palette = extract_palette_from_font(font_file, debug)
            if palette and debug:
                print(f"Extracted palette from font file {font_file}")
        except Exception as e:
            if debug:
                print(f"Error extracting palette from font: {e}")
    
    # If no palette from font, try palette file
    if palette is None and palette_file and os.path.exists(palette_file):
        try:
            palette = load_palette_from_file(palette_file, debug)
            if debug:
                print(f"Loaded palette from {palette_file}")
        except Exception as e:
            if debug:
                print(f"Error loading palette: {e}")
                print("Using default grayscale palette")
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Find all BMP files
    bmp_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.bmp')]
    
    if not bmp_files:
        if debug:
            print(f"No BMP files found in {input_folder}")
        return
    
    if debug:
        print(f"Found {len(bmp_files)} BMP files to convert")
    
    # Convert each BMP file
    for bmp_file in sorted(bmp_files):
        input_path = os.path.join(input_folder, bmp_file)
        output_name = os.path.splitext(bmp_file)[0] + '.png'
        output_path = os.path.join(output_folder, output_name)
        
        try:
            convert_bmp_to_png(input_path, output_path, palette, debug)
        except Exception as e:
            if debug:
                print(f"Error converting {bmp_file}: {e}")

def create_sample_palette_files(debug=False):
    """Create sample palette files for testing"""
    
    # Create JASC-PAL format sample
    with open('sample_palette.pal', 'w') as f:
        f.write('JASC-PAL\n')
        f.write('0100\n')
        f.write('256\n')
        for i in range(256):
            # Simple grayscale palette
            f.write(f'{i} {i} {i}\n')
    
    # Create JSON format sample
    palette_json = {
        "palette": [[i, i, i] for i in range(256)]
    }
    with open('sample_palette.json', 'w') as f:
        json.dump(palette_json, f, indent=2)
    
    # Create binary format sample
    with open('sample_palette.bin', 'wb') as f:
        for i in range(256):
            f.write(bytes([i, i, i]))  # RGB grayscale
    
    if debug:
        print("Created sample palette files:")
        print("  sample_palette.pal (JASC-PAL format)")
        print("  sample_palette.json (JSON format)")
        print("  sample_palette.bin (Binary format)")

def analyze_palette_file(palette_file, debug=False):
    """
    Analyze a palette file to determine its format and show contents
    """
    print(f"Analyzing palette file: {palette_file}")
    print("=" * 50)
    
    if not os.path.exists(palette_file):
        print("File not found!")
        return
    
    file_size = os.path.getsize(palette_file)
    print(f"File size: {file_size} bytes")
    
    # Try to read as text first
    try:
        with open(palette_file, 'rb') as f:
            lines = f.readlines()
        
        print(f"Text file with {len(lines)} lines")
        print("First 10 lines:")
        for i, line in enumerate(lines[:10]):
            print(f"  {i+1:2d}: '{line.rstrip()}'")
        
        if len(lines) > 10:
            print(f"  ... and {len(lines) - 10} more lines")
        
        # Check for JASC-PAL format
        if len(lines) >= 3:
            if lines[0].strip() == 'JASC-PAL':
                print("\n✓ Detected JASC-PAL format")
                version = lines[1].strip()
                try:
                    color_count = int(lines[2].strip())
                    print(f"  Version: {version}")
                    print(f"  Color count: {color_count}")
                    print(f"  Expected total lines: {3 + color_count}")
                except ValueError:
                    print("  ✗ Invalid color count in line 3")
            else:
                print("✗ Not JASC-PAL format (missing 'JASC-PAL' header)")
                print("  Might be raw RGB format")
        
    except UnicodeDecodeError:
        print("Binary file (not text)")
        
        # Check if it's an .act file (768 bytes)
        if file_size == 768:
            print("✓ Might be Adobe Color Table (.act) format")
            with open(palette_file, 'rb') as f:
                first_few = f.read(12)  # First 4 colors
                print("First 4 colors (RGB):")
                for i in range(4):
                    r, g, b = first_few[i*3:(i+1)*3]
                    print(f"  Color {i}: R={r}, G={g}, B={b}")
        else:
            print(f"Binary file with {file_size} bytes")
            if file_size % 3 == 0:
                color_count = file_size // 3
                print(f"✓ Might be raw RGB binary ({color_count} colors)")
            else:
                print("✗ Size not divisible by 3 (unusual for RGB palette)")

def main():
    # Check for debug parameter (can be anywhere in args)
    debug = 'debug' in [arg.lower() for arg in sys.argv]
    args = [arg for arg in sys.argv if arg.lower() != 'debug']  # Remove debug from args
    
    if len(args) < 2:
        print("BMP to PNG Converter with Palette Support")
        print("=" * 50)
        print("")
        print("Usage:")
        print("  Convert single file:")
        print("    python convert_bmp_to_png.py input.bmp [output.png] [palette_file] [debug]")
        print("")
        print("  Convert folder:")
        print("    python convert_bmp_to_png.py folder input_folder output_folder [palette_file] [font_file] [debug]")
        print("")
        print("  Analyze palette file:")
        print("    python convert_bmp_to_png.py analyze palette_file [debug]")
        print("")
        print("  Create sample palette files:")
        print("    python convert_bmp_to_png.py samples [debug]")
        print("")
        print("Supported palette formats:")
        print("  .pal  - JASC-PAL format")
        print("  .act  - Adobe Color Table")  
        print("  .json - Custom JSON format")
        print("  .bin  - Raw RGB binary data")
        print("  .pft  - KQ8 font file (palette extraction)")
        print("")
        print("Examples:")
        print("  python convert_bmp_to_png.py bitmap_001.bmp")
        print("  python convert_bmp_to_png.py bitmap_001.bmp output.png")
        print("  python convert_bmp_to_png.py bitmap_001.bmp output.png palette.pal")
        print("  python convert_bmp_to_png.py bitmap_001.bmp output.png palette.pal debug")
        print("  python convert_bmp_to_png.py folder bitmaps png_output")
        print("  python convert_bmp_to_png.py folder bitmaps png_output palette.pal")
        print("  python convert_bmp_to_png.py folder bitmaps png_output \"\" console.pft debug")
        return
    
    if args[1] == "samples":
        create_sample_palette_files(debug)
        return
    
    if args[1] == "analyze":
        if len(args) < 3:
            print("Usage: python convert_bmp_to_png.py analyze palette_file [debug]")
            return
        analyze_palette_file(args[2], debug)
        return
    
    if args[1] == "folder":
        # Folder conversion mode
        if len(args) < 4:
            print("Error: Folder mode requires input and output folders")
            print("Usage: python convert_bmp_to_png.py folder input_folder output_folder [palette_file] [font_file] [debug]")
            return
        
        input_folder = args[2]
        output_folder = args[3]
        palette_file = args[4] if len(args) > 4 and args[4] != "" else None
        font_file = args[5] if len(args) > 5 else None
        
        if not os.path.exists(input_folder):
            print(f"Error: Input folder '{input_folder}' not found")
            return
        
        convert_folder(input_folder, output_folder, palette_file, font_file, debug)
        
    else:
        # Single file conversion mode
        input_file = args[1]
        output_file = args[2] if len(args) > 2 else None
        palette_file = args[3] if len(args) > 3 else None
        
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found")
            return
        
        # Generate output filename if not provided
        if output_file is None:
            output_file = os.path.splitext(input_file)[0] + '.png'
        
        # Load palette if provided
        palette = None
        if palette_file and os.path.exists(palette_file):
            try:
                if palette_file.endswith('.pft'):
                    palette = extract_palette_from_font(palette_file, debug)
                else:
                    palette = load_palette_from_file(palette_file, debug)
                if debug:
                    print(f"Loaded palette from {palette_file}")
            except Exception as e:
                if debug:
                    print(f"Error loading palette: {e}")
                    print("Using default grayscale palette")
        
        convert_bmp_to_png(input_file, output_file, palette, debug)

if __name__ == "__main__":
    main()