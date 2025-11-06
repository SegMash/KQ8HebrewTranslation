#!/usr/bin/env python3
"""
Simple script to identify what data is written at a specific offset
"""

import struct
import json
import glob
import os
from PIL import Image

def find_offset_242():
    """
    Find exactly what should be at offset 0x242 in font creation
    """
    
    # Load metadata
    with open("font/console_metadata.json", 'r') as meta_file:
        metadata = json.load(meta_file)
    
    # Calculate structure step by step
    pos = 0
    
    print(f"Calculating font file structure to find offset 0x242 (578)...")
    print("=" * 60)
    
    # Header
    pos += 4  # PFON
    pos += 4  # block size + align
    pos += 4  # class version
    print(f"After header: pos = 0x{pos:X} ({pos})")
    
    # Font info (11 fields * 4 bytes = 44 bytes)
    pos += 44
    print(f"After font info: pos = 0x{pos:X} ({pos})")
    
    # Character mapping
    pos += 2  # char count
    pos += 2  # char first
    char_count = metadata['character_mapping']['char_count']
    pos += char_count * 2  # char glyph array
    print(f"After character mapping: pos = 0x{pos:X} ({pos})")
    
    # Glyph array
    glyph_count = metadata['font_info']['glyph_count']
    pos += glyph_count * 8  # each glyph is 8 bytes
    print(f"After glyph array: pos = 0x{pos:X} ({pos})")
    
    # Bitmap array header
    pos += 4  # PBMA
    pos += 4  # unknown
    pos += 4  # head
    pos += 4  # chunks
    pos += 4  # version
    pos += 4  # bitmap count
    print(f"After bitmap array header: pos = 0x{pos:X} ({pos})")
    
    # rmap section
    pos += 4  # rmap tag
    pos += 4  # unknown
    
    # Get actual bitmap count from bitmaps folder
    bitmap_files = glob.glob("bitmaps/bitmap_*.png")
    bitmap_count = len(bitmap_files)
    pos += bitmap_count * 4  # reserved entries
    print(f"After rmap section: pos = 0x{pos:X} ({pos})")
    
    # Check if we're close to target
    target = 0x242
    if pos <= target:
        print(f"Need to check individual bitmaps...")
        
        # Load bitmap info
        bitmap_data_list = []
        for bitmap_file in sorted(bitmap_files):
            filename = os.path.basename(bitmap_file)
            if filename.startswith("bitmap_") and filename.endswith(".png"):
                index_str = filename[7:-4]
                try:
                    index = int(index_str)
                    img = Image.open(bitmap_file)
                    if img.mode != 'L':
                        img = img.convert('L')
                    
                    bitmap_data = {
                        'index': index,
                        'width': img.width,
                        'height': img.height,
                        'data_size': len(list(img.getdata()))
                    }
                    bitmap_data_list.append(bitmap_data)
                except ValueError:
                    pass
        
        bitmap_data_list.sort(key=lambda x: x['index'])
        
        # Process each bitmap
        for i, bitmap in enumerate(bitmap_data_list):
            bitmap_start = pos
            
            # Each bitmap has:
            pos += 4  # PBMP tag
            pos += 4  # unknown
            pos += 4  # head
            pos += 4  # chunks
            pos += 4  # version
            pos += 4  # width (corrected)
            pos += 4  # height
            pos += 4  # bitCount
            pos += 4  # flags
            pos += 4  # data tag
            pos += bitmap['data_size']  # pixel data
            pos += 4  # padding
            pos += 4  # DETL tag
            pos += 4  # mipmap count
            pos += 4  # final padding
            
            bitmap_end = pos
            
            if bitmap_start <= target < bitmap_end:
                offset_in_bitmap = target - bitmap_start
                print(f"\n*** TARGET FOUND at 0x{target:X} ***")
                print(f"Bitmap {i} (index {bitmap['index']})")
                print(f"Bitmap range: 0x{bitmap_start:X} - 0x{bitmap_end-1:X}")
                print(f"Offset in bitmap: {offset_in_bitmap} bytes")
                
                # Break down bitmap structure
                bitmap_pos = bitmap_start
                sections = [
                    ("PBMP tag", 4),
                    ("unknown", 4),
                    ("head", 4),
                    ("chunks", 4),
                    ("version", 4),
                    ("width", 4),
                    ("height", 4),
                    ("bitCount", 4),
                    ("flags", 4),
                    ("data tag", 4),
                    ("pixel data", bitmap['data_size']),
                    ("padding", 4),
                    ("DETL tag", 4),
                    ("mipmap count", 4),
                    ("final padding", 4)
                ]
                
                for section_name, section_size in sections:
                    section_end = bitmap_pos + section_size
                    if bitmap_pos <= target < section_end:
                        offset_in_section = target - bitmap_pos
                        print(f"Section: {section_name}")
                        print(f"Section range: 0x{bitmap_pos:X} - 0x{section_end-1:X}")
                        print(f"Position in section: byte {offset_in_section}")
                        if section_name in ["PBMP tag", "data tag", "DETL tag"]:
                            print(f"This is a 4-byte tag/string")
                        elif section_name == "pixel data":
                            print(f"This is bitmap pixel data")
                        else:
                            print(f"This is a 4-byte integer field")
                        break
                    bitmap_pos = section_end
                break
            
            if i < 5 or bitmap_end > target:  # Show first few or until we pass target
                print(f"Bitmap {i}: 0x{bitmap_start:X} - 0x{bitmap_end-1:X}")
            
            if bitmap_end > target + 100:  # Stop if we're well past target
                break
    
    print(f"\nFinal position: 0x{pos:X} ({pos})")

if __name__ == "__main__":
    find_offset_242()