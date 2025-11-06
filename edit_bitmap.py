#!/usr/bin/env python3
"""
Helper script to edit bitmap files for KQ8 fonts
"""

from PIL import Image, ImageDraw, ImageFont
import sys
import os

def create_hebrew_aleph(width=12, height=15, background_value=0, text_value=157):
    """
    Create a bitmap with Hebrew letter א (Aleph)
    Uses the correct KQ8 font colors: 0=background, 157=text
    """
    # Create background with correct value
    img = Image.new('L', (width, height), background_value)
    
    # Set pixel (0,0) to encode bitmap dimensions: width × height
    # This is part of the KQ8 font format
    img.putpixel((0, 0), width * height)
    
    # Get drawing context
    draw = ImageDraw.Draw(img)
    
    # Draw Hebrew letter א with the correct color values
    aleph_pixels = [
        # Format: (x, y) coordinates for text pixels
        (6, 2),   # Top point
        (5, 3), (6, 3), (7, 3),
        (4, 4), (5, 4),         (8, 4),
        (3, 5), (4, 5),         (8, 5), (9, 5),
        (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6),
        (3, 7),                         (8, 7),
        (3, 8),         (5, 8), (6, 8),         (8, 8),
        (3, 9),         (5, 9), (6, 9),         (8, 9),
        (3, 10),        (5, 10), (6, 10),       (8, 10),
        (3, 11),        (5, 11), (6, 11),       (8, 11),
        (3, 12),        (5, 12), (6, 12),       (8, 12),
    ]
    
    # Draw all pixels with the correct text color (157)
    for x, y in aleph_pixels:
        if 0 <= x < width and 0 <= y < height:
            draw.point((x, y), fill=text_value)  # Use color 157 for text
    
    return img

def edit_bitmap_file(bitmap_path, output_path=None):
    """
    Edit a bitmap file to contain Hebrew letter א
    """
    if not os.path.exists(bitmap_path):
        print(f"Error: {bitmap_path} not found")
        return False
    
    # Load original bitmap to get dimensions and color values
    original = Image.open(bitmap_path)
    width, height = original.size
    
    # Analyze original colors to determine background and text values
    pixels = list(original.getdata())
    unique_values = sorted(set(pixels))
    
    print(f"Original bitmap: {width}x{height}")
    print(f"Original color values: {unique_values}")
    
    # Use the correct KQ8 font colors based on analysis
    background_value = 0   # Background is always 0
    text_value = 157       # Use color 157 as requested by user
    
    print(f"Using background: {background_value}, text: {text_value}")
    
    # Create new bitmap with Hebrew letter
    new_bitmap = create_hebrew_aleph(width, height, background_value, text_value)
    
    # Save to output path
    if output_path is None:
        output_path = bitmap_path
    
    new_bitmap.save(output_path)
    print(f"Saved Hebrew א to: {output_path}")
    
    return True

def preview_bitmap(bitmap_path):
    """
    Preview a bitmap file in the console
    """
    if not os.path.exists(bitmap_path):
        print(f"Error: {bitmap_path} not found")
        return
    
    img = Image.open(bitmap_path)
    pixels = list(img.getdata())
    width, height = img.size
    
    # Determine threshold - use middle value between min and max
    unique_values = sorted(set(pixels))
    if len(unique_values) > 1:
        threshold = (min(unique_values) + max(unique_values)) // 2
    else:
        threshold = 128
    
    print(f"Bitmap preview ({width}x{height}):")
    print(f"Pixel values: {unique_values}")
    print(f"Using threshold: {threshold}")
    print("█ = text (low values), ░ = background (high values)")
    print()
    
    for y in range(height):
        row = ""
        for x in range(width):
            pixel = pixels[y * width + x]
            if pixel <= threshold:  # Low values = text
                row += "█"
            else:  # High values = background
                row += "░"
        print(row)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python edit_bitmap.py <bitmap_file> [output_file]")
        print("  python edit_bitmap.py preview <bitmap_file>")
        print()
        print("Examples:")
        print("  python edit_bitmap.py bitmaps/bitmap_096.png")
        print("  python edit_bitmap.py bitmaps/bitmap_096.png bitmaps/bitmap_096_aleph.png")
        print("  python edit_bitmap.py preview bitmaps/bitmap_096.png")
        return
    
    if sys.argv[1] == "preview":
        if len(sys.argv) < 3:
            print("Usage: python edit_bitmap.py preview <bitmap_file>")
            return
        preview_bitmap(sys.argv[2])
    else:
        bitmap_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        
        if edit_bitmap_file(bitmap_file, output_file):
            # Show preview of the result
            print("\nPreview of new bitmap:")
            preview_bitmap(output_file or bitmap_file)

if __name__ == "__main__":
    main()