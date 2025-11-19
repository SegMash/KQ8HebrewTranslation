#!/usr/bin/env python3
"""
Font Pattern Analyzer for King's Quest 8
Analyzes bitmap font files to understand design patterns from the 90s

This script creates a "union" image showing common patterns across all bitmap files
of a specific width. The union works like an AND operation:
- If all images have the same pixel value at position [x,y], use that value
- If pixels differ across images, use 0 (background)

This reveals the common structure/template that designers used.
"""

import os
import sys
import glob
from PIL import Image
import argparse

def count_black_columns(img):
    """
    Count the number of black columns in an image
    
    Args:
        img: PIL Image object
        
    Returns:
        Number of columns where all pixels are 0 (with special handling for first column)
    """
    pixel_data = list(img.getdata())
    width = img.width
    height = img.height
    black_cols = 0
    
    for x in range(width):
        is_black_col = True
        
        for y in range(height):
            pixel_index = y * width + x
            pixel_value = pixel_data[pixel_index]
            
            # Special case: for first column (x=0), ignore pixel at (0,0) since it's always colored
            if x == 0 and y == 0:
                continue
            
            if pixel_value != 0:
                is_black_col = False
                break
        
        if is_black_col:
            black_cols += 1
    
    return black_cols

def analyze_color_statistics(bitmap_folder, debug=False):
    """
    Analyze color usage statistics across all bitmap images
    
    Args:
        bitmap_folder: Path to folder containing bitmap files
        debug: Whether to print debug information
        
    Returns:
        Dictionary with color statistics
    """
    
    if debug:
        print(f"Analyzing color statistics in: {bitmap_folder}")
        print("=" * 60)
    
    # Find all BMP files
    bmp_pattern = os.path.join(bitmap_folder, "*.bmp")
    all_bmp_files = glob.glob(bmp_pattern)
    
    if not all_bmp_files:
        print(f"No BMP files found in {bitmap_folder}")
        return None
    
    # Color statistics tracking
    color_counts = {}
    total_pixels = 0
    processed_files = 0
    
    for bmp_file in sorted(all_bmp_files):
        try:
            img = Image.open(bmp_file)
            pixel_data = list(img.getdata())
            
            # Count pixels for this image
            for pixel in pixel_data:
                color_counts[pixel] = color_counts.get(pixel, 0) + 1
                total_pixels += 1
            
            processed_files += 1
            
            if debug:
                print(f"  ✓ {os.path.basename(bmp_file)}: {img.width}x{img.height} ({len(pixel_data)} pixels)")
                
        except Exception as e:
            if debug:
                print(f"  ✗ Error loading {os.path.basename(bmp_file)}: {e}")
    
    if total_pixels == 0:
        print("No pixels found to analyze")
        return None
    
    # Calculate statistics
    color_stats = []
    for color, count in color_counts.items():
        percentage = (count / total_pixels) * 100
        color_stats.append({
            'color': color,
            'count': count,
            'percentage': percentage
        })
    
    # Sort by usage (most used first)
    color_stats.sort(key=lambda x: x['count'], reverse=True)
    
    # Print statistics
    print(f"\n📊 Color Usage Statistics")
    print("=" * 60)
    print(f"Total images processed: {processed_files}")
    print(f"Total pixels analyzed: {total_pixels:,}")
    print(f"Unique colors found: {len(color_stats)}")
    print()
    
    print(f"{'Color':<8} {'i':<3} {'j':<3} {'Count':<12} {'Percentage':<12} {'Visual':<20}")
    print("-" * 58)
    
    for stat in color_stats:
        color = stat['color']
        count = stat['count']
        percentage = stat['percentage']
        
        # Calculate i and j values
        i = color // 16 + 1
        j = color % 16 + 1
        
        # Create visual representation (bar chart using characters)
        bar_length = int(percentage / 2)  # Scale down for display
        bar = "█" * min(bar_length, 20)  # Max 20 chars
        
        print(f"{color:<8} {i:<3} {j:<3} {count:<12,} {percentage:<11.2f}% {bar:<20}")
    
    # Additional insights
    print("\n🔍 Insights:")
    most_used = color_stats[0]
    print(f"  Most used color: {most_used['color']} ({most_used['percentage']:.1f}%)")
    
    if len(color_stats) > 1:
        second_most = color_stats[1]
        print(f"  Second most used: {second_most['color']} ({second_most['percentage']:.1f}%)")
    
    # Background vs content analysis
    background_pixels = color_counts.get(0, 0)
    content_pixels = total_pixels - background_pixels
    
    print(f"  Background pixels (0): {background_pixels:,} ({background_pixels/total_pixels*100:.1f}%)")
    print(f"  Content pixels (non-0): {content_pixels:,} ({content_pixels/total_pixels*100:.1f}%)")
    
    # Rare colors (< 1%)
    rare_colors = [s for s in color_stats if s['percentage'] < 1.0]
    if rare_colors:
        print(f"  Rare colors (< 1%): {len(rare_colors)} colors")
    
    return color_stats

def analyze_font_patterns(bitmap_folder, target_width, output_file=None, num_black_cols=None, debug=False):
    """
    Analyze font bitmap patterns and create union image
    
    Args:
        bitmap_folder: Path to folder containing bitmap files
        target_width: Width of bitmaps to analyze
        output_file: Output union image file (optional)
        num_black_cols: Number of black columns to filter by (optional)
        debug: Whether to print debug information
    """
    
    if debug:
        print(f"Analyzing font patterns in: {bitmap_folder}")
        print(f"Target width: {target_width}")
        if num_black_cols is not None:
            print(f"Filter: Only images with exactly {num_black_cols} black columns")
        print("=" * 60)
    
    # Find all BMP files with target width
    bmp_pattern = os.path.join(bitmap_folder, "*.bmp")
    all_bmp_files = glob.glob(bmp_pattern)
    
    if not all_bmp_files:
        print(f"No BMP files found in {bitmap_folder}")
        return False
    
    # Filter by width and collect image data
    matching_images = []
    matching_files = []
    
    for bmp_file in sorted(all_bmp_files):
        try:
            img = Image.open(bmp_file)
            
            if img.width == target_width:
                # Check black columns filter if specified
                if num_black_cols is not None:
                    black_cols = count_black_columns(img)
                    if black_cols != num_black_cols:
                        if debug:
                            print(f"  - {os.path.basename(bmp_file)}: {img.width}x{img.height} (skipped - has {black_cols} black cols, need {num_black_cols})")
                        continue
                
                matching_images.append(img)
                matching_files.append(os.path.basename(bmp_file))
                if debug:
                    black_cols = count_black_columns(img) if num_black_cols is not None else "N/A"
                    print(f"  ✓ {os.path.basename(bmp_file)}: {img.width}x{img.height} (black cols: {black_cols})")
            else:
                if debug:
                    print(f"  - {os.path.basename(bmp_file)}: {img.width}x{img.height} (skipped - wrong width)")
                    
        except Exception as e:
            if debug:
                print(f"  ✗ Error loading {os.path.basename(bmp_file)}: {e}")
    
    if not matching_images:
        print(f"No BMP files with width {target_width} found")
        return False
    
    if debug:
        print(f"\nFound {len(matching_images)} images with width {target_width}")
        print("Files analyzed:")
        for filename in matching_files:
            print(f"  - {filename}")
    
    # Determine dimensions for union image
    # Use the maximum height among all matching images
    max_height = max(img.height for img in matching_images)
    union_width = target_width
    union_height = max_height
    
    if debug:
        print(f"\nUnion image dimensions: {union_width}x{union_height}")
        print("Creating union image...")
    
    # Create union image
    union_pixels = []
    
    for y in range(union_height):
        for x in range(union_width):
            # Collect pixel values from all images at position (x, y)
            pixel_values = []
            
            for img in matching_images:
                if x < img.width and y < img.height:
                    pixel_data = list(img.getdata())
                    pixel_index = y * img.width + x
                    pixel_values.append(pixel_data[pixel_index])
                else:
                    # If image is smaller, treat as 0
                    pixel_values.append(0)
            
            # Apply union logic: find non-zero pixels and check if they're all the same
            non_zero_values = [v for v in pixel_values if v != 0]
            
            if not non_zero_values:
                # All pixels are 0, so union is 0
                union_pixel = 0
            elif len(set(non_zero_values)) == 1:
                # All non-zero pixels have the same color, use that color
                union_pixel = non_zero_values[0]
            else:
                # Non-zero pixels have different colors, use 0
                union_pixel = 0
            
            union_pixels.append(union_pixel)
    
    # Create and save union image
    union_img = Image.new('L', (union_width, union_height))
    union_img.putdata(union_pixels)
    
    # Generate output filename if not provided
    if output_file is None:
        folder_name = os.path.basename(bitmap_folder.rstrip('/\\'))
        output_file = f"font_pattern_w{target_width}_{folder_name}.bmp"
    
    union_img.save(output_file)
    
    if debug:
        print(f"✓ Union image saved: {output_file}")
        
        # Analyze the union image
        unique_values = set(union_pixels)
        non_zero_pixels = sum(1 for p in union_pixels if p != 0)
        total_pixels = len(union_pixels)
        
        print(f"\nUnion Image Analysis:")
        print(f"  Dimensions: {union_width}x{union_height}")
        print(f"  Total pixels: {total_pixels}")
        print(f"  Common pixels: {non_zero_pixels}")
        print(f"  Different pixels: {total_pixels - non_zero_pixels}")
        print(f"  Common coverage: {non_zero_pixels/total_pixels*100:.1f}%")
        print(f"  Unique pixel values: {sorted(unique_values)}")
        
        if non_zero_pixels > 0:
            print(f"\nThis shows the common structure/template used by designers!")
            print(f"Non-zero pixels represent areas where ALL {len(matching_images)} characters")
            print(f"have the same pixel value - revealing the design pattern.")
        else:
            print(f"\nNo common patterns found - characters are very different from each other.")
    
    return True

def create_comparison_grid(bitmap_folder, target_width, output_file=None, num_black_cols=None, debug=False):
    """
    Create a grid showing all matching bitmaps plus the union for comparison
    
    Args:
        bitmap_folder: Path to folder containing bitmap files
        target_width: Width of bitmaps to analyze
        output_file: Output comparison grid file (optional)
        num_black_cols: Number of black columns to filter by (optional)
        debug: Whether to print debug information
    """
    
    # Find all BMP files with target width
    bmp_pattern = os.path.join(bitmap_folder, "*.bmp")
    all_bmp_files = glob.glob(bmp_pattern)
    
    matching_images = []
    matching_files = []
    
    for bmp_file in sorted(all_bmp_files):
        try:
            img = Image.open(bmp_file)
            
            if img.width == target_width:
                # Check black columns filter if specified
                if num_black_cols is not None:
                    black_cols = count_black_columns(img)
                    if black_cols != num_black_cols:
                        continue
                
                matching_images.append(img)
                matching_files.append(os.path.basename(bmp_file))
        except:
            continue
    
    if not matching_images:
        if debug:
            print("No matching images found for comparison grid")
        return False
    
    # Create union image (reuse logic from above)
    max_height = max(img.height for img in matching_images)
    union_pixels = []
    
    for y in range(max_height):
        for x in range(target_width):
            pixel_values = []
            for img in matching_images:
                if x < img.width and y < img.height:
                    pixel_data = list(img.getdata())
                    pixel_index = y * img.width + x
                    pixel_values.append(pixel_data[pixel_index])
                else:
                    pixel_values.append(0)
            
            # Apply same union logic as main function
            non_zero_values = [v for v in pixel_values if v != 0]
            
            if not non_zero_values:
                union_pixels.append(0)
            elif len(set(non_zero_values)) == 1:
                union_pixels.append(non_zero_values[0])
            else:
                union_pixels.append(0)
    
    union_img = Image.new('L', (target_width, max_height))
    union_img.putdata(union_pixels)
    
    # Calculate grid dimensions
    cols = min(8, len(matching_images) + 1)  # +1 for union image
    rows = ((len(matching_images) + 1) + cols - 1) // cols
    
    # Create grid image
    grid_width = cols * (target_width + 2) - 2  # +2 for spacing between images
    grid_height = rows * (max_height + 2) - 2
    grid_img = Image.new('L', (grid_width, grid_height), 128)  # Gray background
    
    # Place images in grid
    images_to_place = matching_images + [union_img]
    labels = matching_files + ["UNION"]
    
    for i, (img, label) in enumerate(zip(images_to_place, labels)):
        row = i // cols
        col = i % cols
        
        x_pos = col * (target_width + 2)
        y_pos = row * (max_height + 2)
        
        grid_img.paste(img, (x_pos, y_pos))
    
    # Generate output filename if not provided
    if output_file is None:
        folder_name = os.path.basename(bitmap_folder.rstrip('/\\'))
        output_file = f"font_comparison_w{target_width}_{folder_name}.bmp"
    
    grid_img.save(output_file)
    
    if debug:
        print(f"✓ Comparison grid saved: {output_file}")
        print(f"  Grid: {cols}x{rows} ({len(images_to_place)} images including union)")
    
    return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Analyze font bitmap patterns to understand 90s design techniques',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_font_patterns.py bitmaps 12
  python analyze_font_patterns.py bitmaps 8 --output font_pattern.bmp
  python analyze_font_patterns.py bitmaps 12 --grid --debug
  python analyze_font_patterns.py bitmaps 12 --num-black-cols 2 --debug
  python analyze_font_patterns.py bitmaps --stats --debug
  
This tool helps understand how designers in the 90s created consistent font patterns
by showing what pixels are common across all characters of the same width.
Black column filter helps analyze characters with specific spacing patterns.
Use --stats to analyze color usage across all bitmap images.
        """
    )
    
    parser.add_argument('bitmap_folder', help='Folder containing bitmap files')
    parser.add_argument('width', type=int, nargs='?', help='Width of bitmaps to analyze (required for pattern analysis)')
    parser.add_argument('--output', '-o', help='Output union image filename')
    parser.add_argument('--num-black-cols', type=int, help='Filter by number of black columns (exact match)')
    parser.add_argument('--grid', action='store_true', help='Also create comparison grid')
    parser.add_argument('--stats', action='store_true', help='Show color usage statistics across all images')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    # Check if folder exists
    if not os.path.exists(args.bitmap_folder):
        print(f"Error: Folder '{args.bitmap_folder}' not found")
        sys.exit(1)
    
    if not os.path.isdir(args.bitmap_folder):
        print(f"Error: '{args.bitmap_folder}' is not a directory")
        sys.exit(1)
    
    # If user just wants color statistics
    if args.stats:
        analyze_color_statistics(args.bitmap_folder, args.debug)
        return
    
    # For pattern analysis, width is required
    if args.width is None:
        parser.error("Width is required for pattern analysis. Use --stats for color statistics only.")
    
    try:
        # Create union image
        success = analyze_font_patterns(args.bitmap_folder, args.width, args.output, args.num_black_cols, args.debug)
        
        if success and args.grid:
            # Also create comparison grid
            grid_output = None
            if args.output:
                base_name = os.path.splitext(args.output)[0]
                grid_output = f"{base_name}_grid.bmp"
            
            create_comparison_grid(args.bitmap_folder, args.width, grid_output, args.num_black_cols, args.debug)
        
        if success:
            print(f"\n🎨 Analysis complete! This reveals the design patterns used by")
            print(f"   90s game developers for creating consistent font characters.")
        
    except Exception as e:
        print(f"Error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()