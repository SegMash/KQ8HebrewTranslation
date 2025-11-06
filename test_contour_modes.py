#!/usr/bin/env python3
"""
Test different contour retrieval modes for Hebrew letters
"""

import cv2
import numpy as np
import os

def test_contour_modes(image_path):
    """
    Test different contour retrieval modes
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Could not load {image_path}")
        return
    
    print(f"Testing contour modes on: {image_path}")
    print(f"Image size: {img.shape[1]}x{img.shape[0]}")
    
    # Create binary image
    _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    
    # Test different retrieval modes
    modes = {
        'RETR_EXTERNAL': cv2.RETR_EXTERNAL,
        'RETR_LIST': cv2.RETR_LIST, 
        'RETR_TREE': cv2.RETR_TREE,
        'RETR_CCOMP': cv2.RETR_CCOMP
    }
    
    for mode_name, mode_value in modes.items():
        contours, _ = cv2.findContours(binary, mode_value, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by area
        significant_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 10:  # Filter tiny contours
                x, y, w, h = cv2.boundingRect(contour)
                significant_contours.append({
                    'area': area,
                    'bbox': (x, y, w, h),
                    'center_x': x + w // 2
                })
        
        # Sort by area and show top contours
        significant_contours.sort(key=lambda x: x['area'], reverse=True)
        
        print(f"\n{mode_name}:")
        print(f"  Total contours: {len(contours)}")
        print(f"  Significant contours (area>10): {len(significant_contours)}")
        
        if len(significant_contours) >= 27:
            print(f"  ✓ Found enough contours for 27 Hebrew letters")
            # Show top 5 contours
            for i, data in enumerate(significant_contours[:5]):
                x, y, w, h = data['bbox']
                print(f"    Top {i+1}: area={data['area']:4.0f}, bbox=({x:3d},{y:2d},{w:2d},{h:2d})")
        else:
            print(f"  ⚠ Only {len(significant_contours)} significant contours (need 27)")

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python test_contour_modes.py <image_path>")
        print("Example: python test_contour_modes.py hebrew_letters/all_letters.png")
        return
    
    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found")
        return
    
    test_contour_modes(image_path)

if __name__ == "__main__":
    main()