#!/usr/bin/env python3
"""
Hebrew Letter Extractor for KQ8 Fonts
Extracts Hebrew letters from a single PNG file and creates individual bitmap files
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw
import os
import sys

def find_contours_in_image(image_path):
    """
    Find the largest 27 contours in the Hebrew letters image
    Returns list of contours with their bounding boxes and Y positions
    """
    # Load image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Error: Could not load image {image_path}")
        return []
    
    print(f"Loaded image: {img.shape[1]}x{img.shape[0]} pixels")
    
    # Threshold the image to create binary image
    # Assuming letters are dark on light background
    _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    
    # Find contours - try different retrieval modes
    # cv2.RETR_LIST finds all contours without hierarchy (might work better for detailed letters)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    print(f"Found {len(contours)} total contours")
    if (len(contours) != 27):
        print("Warning: Expected 27 contours for Hebrew letters, found different number.")
        exit(1)
    
    # Calculate area and bounding box for each contour
    contour_data = []
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        contour_data.append({
            'contour': contour,
            'area': area,
            'bbox': (x, y, w, h),
            'x': x,
            'y': y,
            'width': w,
            'height': h,
            'center_x': x + w // 2
        })
    
    # Sort by area (largest first) and take top 27
    contour_data.sort(key=lambda x: x['area'], reverse=True)
    largest_27 = contour_data[:27]
    
    # Sort by X position (right to left, so we sort by descending X)
    largest_27.sort(key=lambda x: x['center_x'], reverse=True)
    
    print(f"Selected 27 largest contours:")
    for i, data in enumerate(largest_27):
        x, y, w, h = data['bbox']
        print(f"  Letter {i+1:2d}: area={data['area']:4.0f}, bbox=({x:3d},{y:2d},{w:2d},{h:2d})")
    
    return largest_27, img

def create_target_bitmap(contour_data, original_img, target_width, target_height, background_value=0, text_value=157):
    """
    Create a target bitmap with the rectangular region from original image around the contour
    """
    x, y, w, h = contour_data['bbox']
    
    # Create target image
    target_img = Image.new('L', (target_width, target_height), background_value)
    
    # Set pixel (0,0) to encode bitmap dimensions: width × height
    target_img.putpixel((0, 0), target_width * target_height)
    
    # Calculate X offset for centering
    padding_x = (target_width - w) // 2
    target_x = padding_x
    target_y = y  # Keep original Y position as requested
    if target_y == 0:
        target_y+=1
    
    # Extract the rectangular region from original image
    contour_region = original_img[y:y+h, x:x+w]
    
    # Convert original image region to PIL
    region_pil = Image.fromarray(contour_region)
    
    # Convert to target image array
    target_array = np.array(target_img)
    
    # Make sure we don't go out of bounds
    end_y = min(target_y + h, target_height)
    end_x = min(target_x + w, target_width)
    actual_h = end_y - target_y
    actual_w = end_x - target_x
    
    if target_y >= 0 and target_x >= 0 and actual_h > 0 and actual_w > 0:
        # Copy the rectangular region directly from original image
        # Preserve the original pixel values from the source image
        for dy in range(actual_h):
            for dx in range(actual_w):
                orig_pixel = contour_region[dy, dx]
                # Copy the original pixel value directly
                target_array[target_y + dy, target_x + dx] = orig_pixel
    
    # Apply color remapping to the entire target image (except pixel 0,0)
    for y in range(target_height):
        for x in range(target_width):
            if x == 0 and y == 0:
                continue  # Skip the dimension encoding pixel
            
            pixel_value = target_array[y, x]
            
            # Remap colors according to specifications
            if 1 <= pixel_value <= 30:
                target_array[y, x] = 0
            elif 31 <= pixel_value <= 128:
                target_array[y, x] = 0
            elif 128 > pixel_value < 210:
                target_array[y, x] = 0
            else:
                target_array[y, x] = 157
            # pixel_value == 0 remains 0 (background)
    
    return Image.fromarray(target_array)

def extract_hebrew_letters(input_image_path, output_dir="hebrew_letters"):
    """
    Main function to extract Hebrew letters from PNG file
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Find contours
    contour_data, original_img = find_contours_in_image(input_image_path)
    
    if not contour_data:
        print("No contours found!")
        return
    
    print(f"\nCreating individual letter bitmaps...")
    
    created_files = []
    
    for i, data in enumerate(contour_data):
        letter_num = i + 1
        width = data['width']
        
        # Determine target size based on width
        if width <= 6:
            target_width, target_height = 8, 15
        else:
            target_width, target_height = 12, 15
        
        print(f"Letter {letter_num:2d}: width={width:2d} -> target size {target_width}x{target_height}")
        
        # Create bitmap
        bitmap = create_target_bitmap(data, original_img, target_width, target_height)
        
        # Save bitmap with KQ8 font naming convention
        bitmap_index = 95 + letter_num  # Start from bitmap_096.png
        filename = f"bitmap_{bitmap_index:03d}.png"
        output_path = os.path.join(output_dir, filename)
        bitmap.save(output_path)
        created_files.append(output_path)
        
        print(f"  Saved: {filename} ({target_width}x{target_height})")
    
    print(f"\nCompleted! Created {len(created_files)} Hebrew letter bitmaps in '{output_dir}/'")
    
    # Print summary
    size_8x15 = sum(1 for f in created_files if "8x15" in f)
    size_12x15 = sum(1 for f in created_files if "12x15" in f)
    print(f"  {size_8x15} letters with size 8x15")
    print(f"  {size_12x15} letters with size 12x15")
    
    return created_files

def preview_letter(image_path):
    """
    Preview a letter bitmap in console
    """
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found")
        return
    
    img = Image.open(image_path)
    pixels = list(img.getdata())
    width, height = img.size
    
    unique_values = sorted(set(pixels))
    print(f"Letter preview ({width}x{height}):")
    print(f"Pixel values: {unique_values}")
    print("█ = text, ░ = background, ● = dimension encoding at (0,0)")
    print()
    
    for y in range(height):
        row = ""
        for x in range(width):
            pixel = pixels[y * width + x]
            if pixel == 157:  # Text color
                row += "█"
            elif pixel == width * height and x == 0 and y == 0:  # Dimension encoding
                row += "●"  # Special marker for (0,0) pixel
            else:
                row += "░"  # Background
        print(row)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python extract_hebrew_letters.py <input_image> [output_dir]")
        print("  python extract_hebrew_letters.py preview <letter_bitmap>")
        print()
        print("Examples:")
        print("  python extract_hebrew_letters.py hebrew_letters/all_letters.png")
        print("  python extract_hebrew_letters.py hebrew_letters/all_letters.png hebrew_letters")
        print("  python extract_hebrew_letters.py preview hebrew_letters/bitmap_096.png")
        return
    
    if sys.argv[1] == "preview":
        if len(sys.argv) < 3:
            print("Usage: python extract_hebrew_letters.py preview <letter_bitmap>")
            return
        preview_letter(sys.argv[2])
    else:
        input_image = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "hebrew_letters"
        
        if not os.path.exists(input_image):
            print(f"Error: Input image '{input_image}' not found")
            return
        
        extract_hebrew_letters(input_image, output_dir)

if __name__ == "__main__":
    main()