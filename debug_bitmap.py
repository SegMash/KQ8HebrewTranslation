#!/usr/bin/env python3
"""
Debug script to understand the bitmap format
"""

from PIL import Image
import sys

def analyze_bitmap(bitmap_path):
    img = Image.open(bitmap_path)
    pixels = list(img.getdata())
    width, height = img.size
    
    print(f"Bitmap: {bitmap_path}")
    print(f"Size: {width}x{height}")
    print(f"Mode: {img.mode}")
    print(f"Pixel count: {len(pixels)}")
    
    # Show pixel value distribution
    from collections import Counter
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
            row.append(f"{pixel:3d}")
        print(" ".join(row))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_bitmap(sys.argv[1])
    else:
        # Analyze a few key bitmaps
        analyze_bitmap("bitmaps/bitmap_032.png")  # Space
        print("=" * 50)
        analyze_bitmap("bitmaps/bitmap_065.png")  # A
        print("=" * 50)
        analyze_bitmap("bitmaps/bitmap_096.png")  # Backtick