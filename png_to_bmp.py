#!/usr/bin/env python3
"""
PNG to BMP Converter for KQ8 Font Glyphs
Converts PNG glyph files back to BMP format for game resource packing

This script:
1. Scans a glyphs directory for *.png files
2. Examines each PNG file's dimensions
3. Converts PNG to 8-bit BMP format
4. Sets pixel (0,0) to width * height (KQ8 font format requirement)
5. Saves output BMP files to bitmaps folder
"""

import os
import sys
from PIL import Image
import glob

def convert_png_to_bmp(png_file, output_dir="bitmaps", palette_name="daventry", debug=False):
    """
    Convert a PNG glyph file to BMP format for KQ8 fonts
    
    Args:
        png_file: Path to input PNG file
        output_dir: Output directory for BMP files
        palette_name: Palette to use ("daventry" or "castle")
        debug: Whether to print debug information
    """
    try:
        # Load PNG image
        img = Image.open(png_file)
        width, height = img.size
        
        if debug:
            print(f"Processing: {os.path.basename(png_file)} ({width}x{height})")
        
        # Convert to 8-bit grayscale/palette mode if needed
        if img.mode == 'P':
            # If it's already palette mode, convert to L to get indices
            img = img.convert('L')
        elif img.mode in ['RGB', 'RGBA']:
            # Convert RGB/RGBA to grayscale
            img = img.convert('L')
        elif img.mode != 'L':
            # Convert any other mode to grayscale
            img = img.convert('L')
        
        # Get pixel data
        pixel_data = list(img.getdata())
        
        # Apply palette-specific pixel value mappings
        if palette_name == "daventry":
            color1=157
            #color2=156
            color2=157
            color3=76
        elif palette_name == "castle":
            color1=204
            #color2=205
            color2=204
            color3=19
        elif palette_name == "deadcity":
            color1=208
            color2=208
            color3=16
        elif palette_name == "swamp":
            color1=235
            color2=235
            color3=34
        elif palette_name == "gnome":
            color1=172
            color2=172
            color3=54
        else:
            raise ValueError(f"Invalid palette name: {palette_name}. Must be 'daventry' or 'castle'.")
        
        # Daventry palette mappings
        pixel_data = [0 if pixel < 10 else pixel for pixel in pixel_data]
        pixel_data = [10 if pixel == 127 else pixel for pixel in pixel_data]
        pixel_data = [10 if pixel == 195 else pixel for pixel in pixel_data]
        pixel_data = [color1 if pixel == 172 else pixel for pixel in pixel_data]
        pixel_data = [color1 if pixel == 202 else pixel for pixel in pixel_data]
        pixel_data = [color1 if pixel == 213 else pixel for pixel in pixel_data]
        pixel_data = [color2 if pixel == 196 else pixel for pixel in pixel_data]
        pixel_data = [color1 if pixel == 147 else pixel for pixel in pixel_data]
        pixel_data = [color1 if pixel == 134 else pixel for pixel in pixel_data]
        pixel_data = [color3 if pixel == 137 else pixel for pixel in pixel_data]
        
        
        
        
        # Set pixel (0,0) to width * height (KQ8 font format requirement)
        dimension_encoding = width * height
        pixel_data[0] = dimension_encoding
        
        # Create new image with modified data
        output_img = Image.new('L', (width, height))
        output_img.putdata(pixel_data)
        
        # Generate output filename
        base_name = os.path.splitext(os.path.basename(png_file))[0]
        output_file = os.path.join(output_dir, f"{base_name}.bmp")
        
        # Save as BMP
        output_img.save(output_file, 'BMP')
        
        if debug:
            print(f"  → Saved: {output_file}")
            print(f"  → Dimensions: {width}x{height}, encoding: {dimension_encoding}")
        
        return True
        
    except Exception as e:
        if debug:
            print(f"Error processing {png_file}: {e}")
        return False

def process_glyphs_directory(glyphs_dir, output_dir="bitmaps", palette_name="daventry", debug=False):
    """
    Process all PNG files in a glyphs directory
    
    Args:
        glyphs_dir: Directory containing PNG glyph files
        output_dir: Output directory for BMP files
        palette_name: Palette to use ("daventry" or "castle")
        debug: Whether to print debug information
    """
    
    if debug:
        print(f"Scanning glyphs directory: {glyphs_dir}")
        print(f"Output directory: {output_dir}")
        print(f"Using palette: {palette_name}")
        print("=" * 60)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all PNG files
    png_pattern = os.path.join(glyphs_dir, "*.png")
    png_files = glob.glob(png_pattern)
    
    if not png_files:
        if debug:
            print(f"No PNG files found in {glyphs_dir}")
        return
    
    # Sort files for consistent processing order
    png_files.sort()
    
    if debug:
        print(f"Found {len(png_files)} PNG files to process")
        print()
    
    # Process each PNG file
    success_count = 0
    for png_file in png_files:
        if convert_png_to_bmp(png_file, output_dir, palette_name, debug):
            success_count += 1
        if debug:
            print()  # Empty line between files
    
    if debug:
        print("=" * 60)
        print(f"Processing complete!")
        print(f"Successfully converted: {success_count}/{len(png_files)} files")
        print(f"Output directory: {output_dir}")
        
        # Show some statistics
        if success_count > 0:
            bmp_files = glob.glob(os.path.join(output_dir, "*.bmp"))
            print(f"Total BMP files in output directory: {len(bmp_files)}")

def analyze_png_file(png_file, debug=False):
    """
    Analyze a PNG file and show detailed information
    
    Args:
        png_file: Path to PNG file
        debug: Whether to print debug information
    """
    try:
        img = Image.open(png_file)
        width, height = img.size
        
        print(f"File: {png_file}")
        print(f"Dimensions: {width}x{height}")
        print(f"Mode: {img.mode}")
        print(f"Dimension encoding (width*height): {width * height}")
        
        # Show pixel data info
        if img.mode == 'P':
            print("Palette mode - showing palette info:")
            palette = img.getpalette()
            if palette:
                unique_colors = len(set(palette[i:i+3] for i in range(0, len(palette), 3)))
                print(f"  Palette colors: {unique_colors}")
        
        # Show some pixel values
        pixel_data = list(img.getdata())
        print(f"Total pixels: {len(pixel_data)}")
        print(f"Current pixel (0,0): {pixel_data[0]}")
        
        # Show unique pixel values
        unique_values = sorted(set(pixel_data))
        print(f"Unique pixel values: {unique_values[:20]}{'...' if len(unique_values) > 20 else ''}")
        print(f"Value range: {min(unique_values)} - {max(unique_values)}")
        
    except Exception as e:
        print(f"Error analyzing {png_file}: {e}")

def main():
    """Main function"""
    # Check for debug parameter (can be anywhere in args)
    debug = 'debug' in [arg.lower() for arg in sys.argv]
    args = [arg for arg in sys.argv if arg.lower() != 'debug']  # Remove debug from args
    
    if len(args) < 3:
        print("PNG to BMP Converter for KQ8 Font Glyphs")
        print("=" * 45)
        print("")
        print("Usage:")
        print("  Process glyphs directory:")
        print("    python png_to_bmp.py <glyphs_directory> <palette> [output_directory] [debug]")
        print("")
        print("  Analyze single PNG file:")
        print("    python png_to_bmp.py analyze <png_file> [debug]")
        print("")
        print("Arguments:")
        print("  glyphs_directory  - Directory containing PNG glyph files")
        print("  palette          - Palette to use: 'daventry' or 'castle'")
        print("  output_directory - Optional output directory (default: 'bitmaps')")
        print("")
        print("Examples:")
        print("  python png_to_bmp.py glyphs daventry")
        print("  python png_to_bmp.py glyphs castle bitmaps debug")
        print("  python png_to_bmp.py hebrew_letters daventry castle\\bitmaps debug")
        print("  python png_to_bmp.py analyze glyphs/bitmap_096.png debug")
        print("")
        print("Features:")
        print("  - Converts PNG files to 8-bit BMP format")
        print("  - Sets pixel (0,0) to width*height (KQ8 requirement)")
        print("  - Applies palette-specific pixel value mappings")
        print("  - Supports both 'daventry' and 'castle' palettes")
        print("  - Overwrites existing BMP files (no backup)")
        print("  - Processes all *.png files in directory")
        return
    
    if args[1] == "analyze":
        if len(args) < 3:
            print("Usage: python png_to_bmp.py analyze <png_file> [debug]")
            return
        
        png_file = args[2]
        if not os.path.exists(png_file):
            print(f"Error: File '{png_file}' not found")
            return
        
        analyze_png_file(png_file, debug)
        return
    
    # Process glyphs directory
    glyphs_dir = args[1]
    palette_name = args[2]
    output_dir = args[3] if len(args) > 3 else "bitmaps"
    
    # Validate palette name
    #if palette_name not in ["daventry", "castle"]:
    #    print(f"Error: Invalid palette '{palette_name}'. Must be 'daventry' or 'castle'")
    #    return
    
    if not os.path.exists(glyphs_dir):
        print(f"Error: Glyphs directory '{glyphs_dir}' not found")
        return
    
    if not os.path.isdir(glyphs_dir):
        print(f"Error: '{glyphs_dir}' is not a directory")
        return
    
    try:
        process_glyphs_directory(glyphs_dir, output_dir, palette_name, debug)
    except Exception as e:
        print(f"Error: {e}")
        if debug:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()