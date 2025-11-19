import os
from PIL import Image
import numpy as np

# Step 1: Ensure first line is zeros for all PNG glyphs

def is_background_pixel(pixel):
    """Check if a pixel is considered background (black or transparent)"""
    return np.array_equal(pixel, [0, 0, 0]) or np.array_equal(pixel, [0, 4, 0])

def find_top_left_pixel(arr):
    """
    Find the leftmost pixel on the topmost line that contains content.
    Returns: (top_left_x, top_left_y, rgb_color)
    """
    height, width = arr.shape[:2]
    
    # Find leftmost pixel on topmost line (excluding first line which is zeros)
    for y in range(1, height):  # Start from line 1 (skip first line)
        for x in range(width):
            if not is_background_pixel(arr[y, x]):
                rgb_color = arr[y, x]
                return x, y, rgb_color
    
    return -1, -1, [0, 0, 0]  # No pixel found

def count_empty_columns(arr):
    """
    Count how many columns contain only background pixels (zeros).
    Returns: number of columns that are completely empty
    """
    height, width = arr.shape[:2]
    empty_columns = 0
    
    for x in range(width):
        column_is_empty = True
        for y in range(height):
            if not is_background_pixel(arr[y, x]):
                column_is_empty = False
                break
        
        if column_is_empty:
            empty_columns += 1
    
    return empty_columns

def fix_first_line_zeros(src_dir, tgt_dir):
    if not os.path.exists(tgt_dir):
        os.makedirs(tgt_dir)
    for fname in os.listdir(src_dir):
        if fname.lower().endswith('.png'):
            src_path = os.path.join(src_dir, fname)
            tgt_path = os.path.join(tgt_dir, fname)
            img = Image.open(src_path)
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            arr = np.array(img)
            width_orig = arr.shape[1]
            
            # If width is 4, copy as is without any changes
            if width_orig == 4:
                img_fixed = Image.fromarray(arr)
                img_fixed.save(tgt_path)
                continue
            
            # Set first line to zeros (black RGB)
            arr[0, :] = [0, 0, 0]  # RGB black
            empty_cols=count_empty_columns(arr)

            # Adjust columns if needed
            if empty_cols < 2:
                # Pad with 4 empty cols (2 left, 2 right)
                height, width = arr.shape[:2]
                new_arr = np.zeros((height, width + 4, 3), dtype=arr.dtype)
                new_arr[:, 2:width+2] = arr
                arr = new_arr
                empty_cols = count_empty_columns(arr)
            elif empty_cols > 5:
                # Remove cols in multiples of 4 until empty_cols < 6
                while empty_cols > 5:
                    cols_to_remove = min(4, ((empty_cols - 5) // 4 + 1) * 4)
                    left_remove = cols_to_remove // 2
                    right_remove = cols_to_remove // 2
                    height, width = arr.shape[:2]
                    arr = arr[:, left_remove:width-right_remove]
                    empty_cols = count_empty_columns(arr)
            
            width_orig = arr.shape[1]
            
            #print(f"Processing {fname}: width={width_orig}, empty_columns={empty_cols}")
            required_x_left = 0
            if width_orig >= 12:
                if empty_cols == 5:
                    required_x_left=3
                elif empty_cols == 4:
                    required_x_left = 3
                elif empty_cols == 2 or empty_cols == 3:
                    required_x_left = 4
            elif width_orig == 8:
                if empty_cols == 2:
                    required_x_left = 4
                elif empty_cols == 3:
                    required_x_left = 4
                elif empty_cols == 4:
                    required_x_left = 3
                elif empty_cols == 6:
                    required_x_left = 3
                elif empty_cols == 5:
                    required_x_left = 3
                elif empty_cols == 1:
                    required_x_left = 4

            if "098" in fname:
                print(f"Debug: Processing {fname} with width {width_orig} and empty columns {empty_cols} and required_x_left {required_x_left}")
                
            # Find top-left pixel
            top_left_x, top_left_y, rgb_color = find_top_left_pixel(arr)
            shift_amount = required_x_left
            
            # Create a wider bitmap to accommodate the shift
            height, width = arr.shape[:2]
            new_width = width + shift_amount
            wider_arr = np.zeros((height, new_width, 3), dtype=arr.dtype)
            wider_arr[:, :] = [0, 0, 0]  # Fill with black background
            
            # Copy original image shifted to the right
            wider_arr[:, shift_amount:shift_amount+width] = arr
            
            # Cut the right part that extends beyond original width
            cut_part = wider_arr[:, width:]
            
            # Create final array with original dimensions
            final_arr = np.zeros_like(arr)
            final_arr[:, :] = [0, 0, 0]
            
            # Copy the left part (within original width)
            final_arr[:, :] = wider_arr[:, :width]
            
            # Draw the cut part on x=0 and y+1 (shift down by 1 line)
            if cut_part.shape[1] > 0:  # If there's actually something to wrap
                for y in range(height - 1):  # Don't go beyond image bounds
                    for x in range(min(cut_part.shape[1], width)):
                        if not is_background_pixel(cut_part[y, x]):
                            final_arr[y + 1, x] = cut_part[y, x]

            arr = final_arr
            
            img_fixed = Image.fromarray(arr)
            img_fixed.save(tgt_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python fix_glyph.py <source_dir> <target_dir>")
        sys.exit(1)
    src_dir = sys.argv[1]
    tgt_dir = sys.argv[2]
    fix_first_line_zeros(src_dir, tgt_dir)
    print(f"Processed all PNG files from {src_dir} to {tgt_dir}, first line set to zeros.")
