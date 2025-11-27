import os
from PIL import Image
import numpy as np
import sys

def count_empty_columns_indexed(arr):
    """
    Count how many columns contain only palette index 0 (background).
    For indexed color images.
    Returns: number of columns that are completely empty
    """
    height, width = arr.shape[:2] if len(arr.shape) > 1 else (1, arr.shape[0])
    empty_columns = 0
    
    for x in range(width):
        column_is_empty = True
        for y in range(height):
            if arr[y, x] != 0:  # Not palette index 0
                column_is_empty = False
                break
        
        if column_is_empty:
            empty_columns += 1
    
    return empty_columns

def shift_image_left_and_wrap_indexed(arr, shift_amount):
    """
    Shift the image left by shift_amount columns and wrap the left part to the right side,
    shifted up by 1 pixel. For indexed color images (8-bit).
    
    Args:
        arr: numpy array of the image (palette indices)
        shift_amount: number of columns to shift
    
    Returns:
        modified array
    """
    height, width = arr.shape[:2] if len(arr.shape) > 1 else (1, arr.shape[0])
    
    # Save the leftmost columns
    left_part = arr[:, :shift_amount].copy()
    
    # Shift the rest of the image left
    arr[:, :width-shift_amount] = arr[:, shift_amount:]
    
    # Fill the rightmost columns with palette index 0 (black)
    arr[:, width-shift_amount:] = 0
    
    # Place the saved left part on the right side, shifted up by 1 pixel
    for y in range(height):
        for x in range(shift_amount):
            if left_part[y, x] != 0:  # Not background
                # Shift up by 1: if y > 0, place at y-1
                if y > 0:
                    arr[y - 1, width - shift_amount + x] = left_part[y, x]
    
    return arr

def reverse_glyph(input_path, output_path, mask_output_path=None, fixed_width=None):
    """
    Reverse the glyph processing:
    1. Zero the first 2 pixels in the first line
    2. Count black columns
    3. Optionally pad to fixed width
    4. Optionally create mask image
    """
    img = Image.open(input_path)
    
    # Save original image properties
    original_mode = img.mode
    
    
    # Get pixel data as-is without any conversion
    arr = np.array(img, dtype=np.uint8)

    # Check if color 224 exists in the array
    if 224 in arr:
        print(f"  Color 224 found in source image")
    
    width = arr.shape[1]
    
    # Step 1: Zero the first 2 pixels in the first line (set to palette index 0)
    arr[0, :2] = 0

    if 224 not in arr:
        print(f"  Color 224 NOT found in source image")
    
    # Step 2: Count black columns (columns with only palette index 0)
    empty_cols = count_empty_columns_indexed(arr)
    
    print(f"Processing {os.path.basename(input_path)}: width={width}, empty_columns={empty_cols}")
    
    # Step 3: If empty_cols == 2, shift left by 4 and wrap to right side shifted up by 1
    if empty_cols == 2:
        arr = shift_image_left_and_wrap_indexed(arr, 4)
    elif empty_cols == 4 or empty_cols == 3:
        arr = shift_image_left_and_wrap_indexed(arr, 3)
    elif empty_cols == 5:
        arr = shift_image_left_and_wrap_indexed(arr, 2)
    
    # Step 4: Change all pixels with color 58 to 0
    #arr[arr == 58] = 0
    #arr[arr < 120] = 0
    #arr[arr > 221] = 0
    
    # Step 4.5: Create mask image before padding (all non-zero colors become 255)
    if mask_output_path is not None:
        mask_arr = arr.copy()
        mask_arr[mask_arr != 0] = 255
    
    # Step 5: Pad to fixed width if specified
    if fixed_width is not None:
        current_width = arr.shape[1]
        if current_width < fixed_width:
            padding_needed = fixed_width - current_width
            left_pad = padding_needed // 2
            right_pad = padding_needed - left_pad
            
            height = arr.shape[0]
            new_arr = np.zeros((height, fixed_width), dtype=arr.dtype)
            new_arr[:, left_pad:left_pad+current_width] = arr
            arr = new_arr
            
            # Also pad mask image if it exists
            if mask_output_path is not None:
                new_mask_arr = np.zeros((height, fixed_width), dtype=mask_arr.dtype)
                new_mask_arr[:, left_pad:left_pad+current_width] = mask_arr
                mask_arr = new_mask_arr
            
            print(f"  Padded from {current_width} to {fixed_width} (left={left_pad}, right={right_pad})")
    
    # Create output image with exact same mode as input
    img_result = Image.fromarray(arr)
    img_result.save(output_path)
    
    # Save mask image if requested
    if mask_output_path is not None:
        mask_result = Image.fromarray(mask_arr)
        mask_result.save(mask_output_path)
    
    return empty_cols

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Reverse glyph processing for bitmap files')
    parser.add_argument('input_dir', help='Input directory containing BMP files')
    parser.add_argument('output_dir', help='Output directory for processed BMP files')
    parser.add_argument('--mask_output_dir', help='Output directory for mask images (all non-zero colors become 255)')
    parser.add_argument('--fixed_width', type=int, help='Pad images to this fixed width (optional)')
    parser.add_argument('--from', dest='from_index', type=int, help='Process bitmaps starting from this index (optional)')
    parser.add_argument('--to', dest='to_index', type=int, help='Process bitmaps up to this index (optional)')
    
    args = parser.parse_args()
    
    input_dir = args.input_dir
    output_dir = args.output_dir
    mask_output_dir = args.mask_output_dir
    fixed_width = args.fixed_width
    from_index = args.from_index
    to_index = args.to_index
    
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' not found")
        sys.exit(1)
    
    if not os.path.isdir(input_dir):
        print(f"Error: '{input_dir}' is not a directory")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Create mask output directory if specified
    if mask_output_dir is not None:
        if not os.path.exists(mask_output_dir):
            os.makedirs(mask_output_dir)
            print(f"Created mask output directory: {mask_output_dir}")
    
    if fixed_width:
        print(f"Fixed width mode: padding images to {fixed_width} pixels")
    
    if from_index is not None or to_index is not None:
        range_str = f"from {from_index if from_index is not None else 'start'} to {to_index if to_index is not None else 'end'}"
        print(f"Index range filter: {range_str}")
    
    # Process all BMP files in input directory
    processed_count = 0
    skipped_count = 0
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.bmp'):
            # If range filter is active, check if filename matches bitmap_###.bmp pattern
            if from_index is not None or to_index is not None:
                if filename.lower().startswith('bitmap_') and filename.lower().endswith('.bmp'):
                    try:
                        # Extract index from bitmap_###.bmp (always 3 digits)
                        # Pattern: bitmap_079.bmp -> extract "079"
                        index_str = filename[7:10]  # Get the ### part (positions 7,8,9)
                        file_index = int(index_str)
                        
                        # Check if index is within range
                        if from_index is not None and file_index < from_index:
                            skipped_count += 1
                            continue
                        if to_index is not None and file_index > to_index:
                            skipped_count += 1
                            continue
                    except (ValueError, IndexError):
                        # If we can't parse the index, skip this file when range is specified
                        skipped_count += 1
                        continue
                else:
                    # Filename doesn't match pattern, skip when range is specified
                    skipped_count += 1
                    continue
            
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            mask_output_path = os.path.join(mask_output_dir, filename) if mask_output_dir else None
            
            try:
                empty_cols = reverse_glyph(input_path, output_path, mask_output_path, fixed_width)
                processed_count += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    if skipped_count > 0:
        print(f"\nSkipped {skipped_count} files outside range.")
    print(f"Done. Processed {processed_count} files.")
