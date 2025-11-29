#!/usr/bin/env python3
"""
Draw Hebrew text on a bitmap by compositing individual letter bitmaps.
Hebrew is Right-To-Left, so letters are drawn from right to left.

The script maps Hebrew characters to bitmap files using Windows-1255 encoding:
  Windows-1255 code - 32 = bitmap number
  Example: א (Windows-1255: 128) -> 128 - 32 = 96 -> bitmap_096.bmp

Usage: python draw_text_on_bitmap.py <main_bitmap> <text> <letters_folder> <x> <y>
"""

import sys
import os
from PIL import Image


def get_bitmap_index(char):
    """
    Get the bitmap index for a character using Windows-1255 encoding.
    
    Args:
        char: Single character
        
    Returns:
        Bitmap index (Windows-1255 code - 32)
    """
    # Encode the character using Windows-1255 and get its byte value
    try:
        win1255_code = char.encode('windows-1255')[0]
    except (UnicodeEncodeError, IndexError):
        # If character cannot be encoded in Windows-1255, fall back to ord()
        win1255_code = ord(char)
    
    return win1255_code - 32


def draw_text_on_bitmap(main_bitmap_path, text, letters_folder, start_x, start_y, output_path=None):
    """
    Draw Hebrew text on a main bitmap using individual letter bitmaps.
    
    Args:
        main_bitmap_path: Path to the main 800x600 bitmap
        text: Hebrew text string to draw
        letters_folder: Folder containing letter bitmap files (bitmap_XXX.bmp)
        start_x: Starting X coordinate (rightmost position for RTL)
        start_y: Starting Y coordinate (top position)
        output_path: Optional output path (defaults to overwriting main_bitmap)
    """
    try:
        # Load the main bitmap
        main_img = Image.open(main_bitmap_path)
        
        # Convert to palette mode if not already (8-bit)
        if main_img.mode != 'P' and main_img.mode != 'L':
            print(f"Warning: Main image mode is {main_img.mode}, converting to 'L' (8-bit grayscale)")
            main_img = main_img.convert('L')
        
        # Save original mode and palette
        original_mode = main_img.mode
        original_palette = None
        if original_mode == 'P':
            original_palette = main_img.getpalette()
        
        print(f"Main bitmap: {main_bitmap_path}")
        print(f"  Size: {main_img.size}")
        print(f"  Mode: {main_img.mode}")
        print(f"Text: '{text}'")
        print(f"Starting position: ({start_x}, {start_y})")
        print(f"Letters folder: {letters_folder}")
        print()
        
        # Get main image data once at the beginning
        main_img_data = list(main_img.getdata())
        main_width, main_height = main_img.size
        
        # Current X position (start from right for RTL)
        current_x = start_x
        current_y = start_y
        
        # Process each character in the text (Hebrew is RTL)
        for i, char in enumerate(text):
            # Skip spaces - just move position
            if char == ' ':
                space_width = 8  # Default space width
                current_x -= space_width
                print(f"Character {i+1}: SPACE - moving left by {space_width} pixels, new X: {current_x}")
                continue
            
            # Get bitmap index for this character
            bitmap_index = get_bitmap_index(char)
            letter_filename = os.path.join(letters_folder, f"bitmap_{bitmap_index:03d}.bmp")
            
            # Check if letter bitmap exists
            if not os.path.exists(letter_filename):
                try:
                    win1255_code = char.encode('windows-1255')[0]
                except:
                    win1255_code = ord(char)
                print(f"Warning: Letter bitmap not found: {letter_filename} (char: '{char}', windows-1255: {win1255_code})")
                continue
            
            # Load the letter bitmap
            letter_img = Image.open(letter_filename)
            
            # Convert letter to same mode as main image
            #if letter_img.mode != original_mode:
            #    if original_mode == 'L':
            #        letter_img = letter_img.convert('L')
            #    elif original_mode == 'P':
            #        letter_img = letter_img.convert('P')
           # 
            letter_width, letter_height = letter_img.size
            
            # For RTL, we need to place the letter to the left of current position
            # So we first move left by the letter width, then paste
            paste_x = current_x - letter_width
            paste_y = current_y
            
            try:
                win1255_code = char.encode('windows-1255')[0]
            except:
                win1255_code = ord(char)
            
            print(f"Character {i+1}: '{char}' (windows-1255: {win1255_code}) -> bitmap_{bitmap_index:03d}.bmp")
            print(f"  Letter size: {letter_width}x{letter_height}")
            print(f"  Paste position: ({paste_x}, {paste_y})")
            
            # Check if position is within bounds
            if paste_x < 0:
                print(f"  Warning: X position {paste_x} is out of bounds (< 0), skipping")
                break
            if paste_y + letter_height > main_img.size[1]:
                print(f"  Warning: Y position {paste_y}+{letter_height} exceeds image height, skipping")
                break
            
            # Paste the letter onto the main image
            # Only draw pixels with specific color values
            valid_colors = {14, 16, 17, 21, 23, 30, 38, 39, 46, 114, 115, 116, 135, 136, 137, 138, 139, 153, 154, 159, 209, 219}
            
            # Get letter pixel data
            letter_data = list(letter_img.getdata())
            if bitmap_index == 14:
                paste_x+=2
            # Draw only the valid color pixels
            for y in range(letter_height):
                for x in range(letter_width):
                    pixel_index = y * letter_width + x
                    pixel_value = letter_data[pixel_index]
                    
                    # Only draw if pixel is one of the valid colors
                    if pixel_value in valid_colors:
                        target_x = paste_x + x
                        target_y = paste_y + y
                        
                        # Check bounds
                        if 0 <= target_x < main_width and 0 <= target_y < main_height:
                            # Calculate index in main image data
                            main_index = target_y * main_width + target_x
                            main_img_data[main_index] = pixel_value
            
            # Move current position left by the letter width (RTL)
            current_x = paste_x
            
            # Special case: if this was bitmap_122, move 3 pixels to the right for the next letter
            if bitmap_index == 122:
                current_x += 3
            elif bitmap_index == 116:
                current_x += 2
            elif bitmap_index == 121:
                current_x += 1
            
            print(f"  New X position: {current_x}")
        
        print()
        print(f"Final X position: {current_x}")
        
        # Update the main image with all the modified data
        main_img.putdata(main_img_data)
        
        # Restore original palette if needed
        #if original_mode == 'P' and original_palette:
        #    main_img.putpalette(original_palette)
        
        # Save the result
        if output_path is None:
            output_path = main_bitmap_path
        
        main_img.save(output_path)
        print(f"\n✓ Text drawn successfully: {output_path}")
        
        return True
        
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        return False
    except PermissionError as e:
        print(f"Error: Permission denied - {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) not in [6, 7]:
        print("Draw Hebrew text on a bitmap using individual letter bitmaps")
        print()
        print("Usage: python draw_text_on_bitmap.py <main_bitmap> <text_file> <letters_folder> <x> <y> [output]")
        print()
        print("Arguments:")
        print("  main_bitmap    - Path to main 800x600 8-bit bitmap")
        print("  text_file      - Path to UTF-8 text file containing Hebrew text to draw (RTL)")
        print("  letters_folder - Folder containing letter bitmaps (bitmap_XXX.bmp)")
        print("  x              - Starting X coordinate (rightmost position)")
        print("  y              - Starting Y coordinate (top position)")
        print("  output         - Optional output path (defaults to overwriting main_bitmap)")
        print()
        print("Letter bitmap naming:")
        print("  Character Windows-1255 code - 32 = bitmap index")
        print("  Example: א (Windows-1255: 128) -> bitmap_096.bmp")
        print()
        print("Example:")
        print("  python draw_text_on_bitmap.py main.bmp credit_text.txt bitmap_credit 400 300")
        print("  python draw_text_on_bitmap.py main.bmp credit_text.txt bitmap_credit 400 300 output.bmp")
        sys.exit(1)
    
    main_bitmap_path = sys.argv[1]
    text_file_path = sys.argv[2]
    letters_folder = sys.argv[3]
    
    # Read text from file
    try:
        with open(text_file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Text file not found: {text_file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading text file: {e}")
        sys.exit(1)
    
    try:
        start_x = int(sys.argv[4])
        start_y = int(sys.argv[5])
    except ValueError:
        print("Error: X and Y coordinates must be integers")
        sys.exit(1)
    
    output_path = sys.argv[6] if len(sys.argv) == 7 else None
    
    # Validate files exist
    if not os.path.exists(main_bitmap_path):
        print(f"Error: Main bitmap does not exist: {main_bitmap_path}")
        sys.exit(1)
    
    if not os.path.exists(letters_folder):
        print(f"Error: Letters folder does not exist: {letters_folder}")
        sys.exit(1)
    
    if not os.path.isdir(letters_folder):
        print(f"Error: Letters folder is not a directory: {letters_folder}")
        sys.exit(1)
    
    # Draw text
    success = draw_text_on_bitmap(main_bitmap_path, text, letters_folder, start_x, start_y, output_path)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
