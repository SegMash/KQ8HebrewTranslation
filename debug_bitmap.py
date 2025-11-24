#!/usr/bin/env python3
"""
Debug script to understand the bitmap format
Supports analyzing individual bitmaps or a range of letter indices
"""

from PIL import Image
import sys
import os
from collections import Counter

def analyze_bitmap(bitmap_path):
    img = Image.open(bitmap_path)
    pixels = list(img.getdata())
    width, height = img.size
    
    print(f"Bitmap: {bitmap_path}")
    print(f"Size: {width}x{height}")
    print(f"Mode: {img.mode}")
    print(f"Pixel count: {len(pixels)}")
    
    # Show pixel value distribution
    pixel_counts = Counter(pixels)
    print("Pixel value distribution:")
    for value, count in sorted(pixel_counts.items()):
        print(f"  {value}: {count} pixels ({count/len(pixels)*100:.1f}%)")
    
    print()
    print("Raw pixel grid (showing actual values):")
    for y in range(height):
        row = []
        for x in range(width):
            pixel = pixels[y * width + x]
            # Handle both indexed color (single int) and RGB (tuple)
            if isinstance(pixel, tuple):
                # For RGB, show as (R,G,B)
                row.append(f"{str(pixel):15s}")
            else:
                # For indexed color, show as single number
                row.append(f"{pixel:3d}")
        print(" ".join(row))

def analyze_bitmap_range(bitmaps_dir, start_index, end_index):
    """Analyze a range of bitmaps and provide summary statistics"""
    print(f"Analyzing bitmaps {start_index} to {end_index} in {bitmaps_dir}")
    print("=" * 60)
    
    total_pixel_counts = Counter()
    total_pixels = 0
    files_analyzed = 0
    
    for letter_index in range(start_index, end_index + 1):
        # Try both .bmp and .png extensions
        bitmap_path_bmp = os.path.join(bitmaps_dir, f"bitmap_{letter_index:03d}.bmp")
        bitmap_path_png = os.path.join(bitmaps_dir, f"bitmap_{letter_index:03d}.png")
        
        bitmap_path = None
        if os.path.exists(bitmap_path_bmp):
            bitmap_path = bitmap_path_bmp
        elif os.path.exists(bitmap_path_png):
            bitmap_path = bitmap_path_png
        else:
            print(f"Warning: Bitmap {letter_index:03d} not found")
            continue
        
        try:
            img = Image.open(bitmap_path)
            pixels = list(img.getdata())
            
            # Accumulate pixel counts
            pixel_counts = Counter(pixels)
            total_pixel_counts.update(pixel_counts)
            total_pixels += len(pixels)
            files_analyzed += 1
            
        except Exception as e:
            print(f"Error processing {bitmap_path}: {e}")
    
    print(f"\nFiles analyzed: {files_analyzed}")
    print(f"Total pixels: {total_pixels}")
    print()
    print("Combined Pixel Value Distribution:")
    print("-" * 60)
    for value, count in sorted(total_pixel_counts.items()):
        percentage = count / total_pixels * 100
        print(f"  Pixel value {value:3d}: {count:6d} pixels ({percentage:5.2f}%)")

if __name__ == "__main__":
    if len(sys.argv) == 4:
        # Range mode: bitmaps_dir start_index end_index
        bitmaps_dir = sys.argv[1]
        start_index = int(sys.argv[2])
        end_index = int(sys.argv[3])
        analyze_bitmap_range(bitmaps_dir, start_index, end_index)
    elif len(sys.argv) == 2:
        # Single bitmap mode
        analyze_bitmap(sys.argv[1])
    else:
        print("Usage:")
        print("  Single bitmap: python debug_bitmap.py <bitmap_path>")
        print("  Range mode: python debug_bitmap.py <bitmaps_dir> <start_index> <end_index>")
        print()
        print("Examples:")
        print("  python debug_bitmap.py bitmaps/bitmap_065.bmp")
        print("  python debug_bitmap.py bitmaps 96 122")