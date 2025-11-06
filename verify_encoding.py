#!/usr/bin/env python3
"""
Verify the 0,0 pixel width encoding theory
"""

from PIL import Image
import os

def verify_width_encoding():
    """
    Check if pixel(0,0) encodes the bitmap width
    """
    print("Verifying width encoding theory:")
    print("pixel(0,0) should equal width × height")
    print("=" * 50)
    
    correct_predictions = 0
    total_bitmaps = 0
    exceptions = []
    
    for i in range(224):
        bitmap_file = f"bitmap_{i:03d}.png"
        bitmap_path = os.path.join("bitmaps", bitmap_file)
        
        if os.path.exists(bitmap_path):
            img = Image.open(bitmap_path)
            width, height = img.size
            first_pixel = img.getpixel((0, 0))
            
            expected = width * height
            actual = first_pixel
            
            total_bitmaps += 1
            
            if actual == expected:
                correct_predictions += 1
            else:
                exceptions.append((i, width, height, expected, actual))
                if len(exceptions) <= 10:  # Show first 10 exceptions
                    print(f"  Exception bitmap_{i:03d}: {width}x{height}, expected={expected}, actual={actual}")
    
    print(f"\nResults:")
    print(f"  Correct predictions: {correct_predictions}/{total_bitmaps} ({correct_predictions/total_bitmaps*100:.1f}%)")
    print(f"  Exceptions: {len(exceptions)}")
    
    if len(exceptions) > 10:
        print(f"  (showing first 10 exceptions only)")

if __name__ == "__main__":
    verify_width_encoding()