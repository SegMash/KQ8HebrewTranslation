#!/usr/bin/env python3
"""
Convert a 24-bit RGB image to 8-bit indexed color using a specific palette file
"""

from PIL import Image
import sys
import numpy as np

def load_palette(palette_file):
    """Load palette from .pal file"""
    with open(palette_file, 'r') as f:
        lines = f.readlines()
    
    # Skip header lines (JASC-PAL format)
    if lines[0].strip() == 'JASC-PAL':
        start_line = 3
    else:
        start_line = 0
    
    palette = []
    for line in lines[start_line:]:
        line = line.strip()
        if line:
            parts = line.split()
            if len(parts) >= 3:
                r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
                palette.extend([r, g, b])
    
    # Ensure palette has exactly 768 values (256 colors * 3 RGB)
    while len(palette) < 768:
        palette.extend([0, 0, 0])
    
    return palette[:768]

def convert_to_palette(input_image, output_image, palette_file):
    """Convert 24-bit image to 8-bit using specific palette"""
    
    # Load the palette
    palette_data = load_palette(palette_file)
    print(f"Loaded palette from {palette_file}")
    
    # Convert palette to numpy array for faster processing
    palette_rgb = np.array(palette_data).reshape(256, 3)
    
    # Open the input image
    img = Image.open(input_image)
    
    # Convert to RGB if needed
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    print(f"Input image: {img.size[0]}x{img.size[1]}, mode: {img.mode}")
    
    # Get pixel data
    pixels = np.array(img)
    height, width = pixels.shape[:2]
    
    print("Converting pixels to palette indices (this may take a moment)...")
    
    # Reshape pixels to (height*width, 3) for vectorized distance calculation
    pixels_flat = pixels.reshape(-1, 3).astype(np.float32)
    
    # Use PIL's built-in quantize with custom palette for much faster conversion
    # Create a palette image
    palette_img = Image.new('P', (1, 1))
    palette_img.putpalette(palette_data)
    
    # Convert the image to use this palette
    output_img = img.quantize(palette=palette_img, dither=0)
    
    print(f"Conversion complete!")
    
    # Save as PNG
    output_img.save(output_image, 'PNG')
    print(f"Saved 8-bit indexed PNG to {output_image}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert 24-bit RGB image to 8-bit indexed color using a specific palette')
    parser.add_argument('input_image', help='Input 24-bit image')
    parser.add_argument('output_image', help='Output 8-bit PNG')
    parser.add_argument('palette_file', help='Palette file (.pal)')
    parser.add_argument('--width', type=int, help='Resize to this width (optional)')
    parser.add_argument('--height', type=int, help='Resize to this height (optional)')
    
    args = parser.parse_args()
    
    # Load and optionally resize before converting
    img = Image.open(args.input_image)
    
    if args.width or args.height:
        original_size = img.size
        new_width = args.width if args.width else img.size[0]
        new_height = args.height if args.height else img.size[1]
        
        print(f"Resizing from {original_size[0]}x{original_size[1]} to {new_width}x{new_height}")
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save resized image temporarily
        temp_file = "temp_resized.png"
        img.save(temp_file)
        input_to_convert = temp_file
    else:
        input_to_convert = args.input_image
    
    convert_to_palette(input_to_convert, args.output_image, args.palette_file)
    
    # Clean up temp file if it was created
    if args.width or args.height:
        import os
        os.remove(temp_file)
    
    print("Done!")
