#!/usr/bin/env python3
"""
Debug script to trace font file creation and find what's at offset 0x242
"""

import struct
import json
import glob
import os
from PIL import Image

def debug_font_creation(metadata_filename, bitmaps_folder):
    """
    Debug font creation to show what data is written at each offset
    """
    
    # Load metadata
    with open(metadata_filename, 'r') as meta_file:
        metadata = json.load(meta_file)
    
    # Scan bitmaps folder
    bitmap_files = glob.glob(os.path.join(bitmaps_folder, "bitmap_*.png"))
    bitmap_files.sort()
    
    bitmap_data_list = []
    for bitmap_file in bitmap_files:
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
                    'data': list(img.getdata())
                }
                bitmap_data_list.append(bitmap_data)
            except ValueError:
                pass
    
    bitmap_data_list.sort(key=lambda x: x['index'])
    
    # Calculate what should be at offset 0x242 (578 decimal)
    target_offset = 0x242
    current_pos = 0
    
    print(f"Tracing font file creation to find offset 0x{target_offset:X} ({target_offset})")
    print("=" * 60)
    
    def trace_write(data_desc, size, data_preview=None):
        nonlocal current_pos
        end_pos = current_pos + size
        if current_pos <= target_offset < end_pos:
            offset_in_section = target_offset - current_pos
            print(f"*** TARGET FOUND at 0x{target_offset:X} ({target_offset}) ***")
            print(f"Section: {data_desc}")
            print(f"Section range: 0x{current_pos:X}-0x{end_pos-1:X}")
            print(f"Position in section: byte {offset_in_section}")
            if data_preview:
                print(f"Data preview: {data_preview}")
            print("=" * 60)
            return True
        elif current_pos <= target_offset <= end_pos:
            print(f"0x{current_pos:03X}-0x{end_pos-1:03X}: {data_desc} *** CONTAINS TARGET ***")
        else:
            print(f"0x{current_pos:03X}-0x{end_pos-1:03X}: {data_desc}")
        current_pos = end_pos
        return False
    
    # Trace the file structure
    trace_write("Block tag (PFON)", 4, "PFON")
    trace_write("Block size + align", 4)
    trace_write("Class version", 4)
    
    # Font info (44 bytes total)
    trace_write("Font flags", 4)
    trace_write("Text flags", 4)
    trace_write("Glyph count", 4)
    trace_write("Char height", 4)
    trace_write("Char width", 4)
    trace_write("Text color", 4)
    trace_write("Back color", 4)
    trace_write("Baseline", 4)
    trace_write("Text H scale", 4)
    trace_write("Text V scale", 4)
    trace_write("Char H space", 4)
    
    # Character mapping
    trace_write("Char count", 2)
    trace_write("Char first", 2)
    
    # Character glyph mapping array
    char_count = metadata['character_mapping']['char_count']
    trace_write(f"Char glyph mapping array ({char_count} entries)", char_count * 2)
    
    # Glyph info array  
    glyph_count = metadata['font_info']['glyph_count']
    trace_write(f"Glyph info array ({glyph_count} entries)", glyph_count * 8)
    
    # Bitmap array header
    trace_write("PBMA tag", 4, "PBMA")
    trace_write("PBMA unknown", 4)
    trace_write("PBMA head", 4)
    trace_write("Bitmap chunks", 4)
    trace_write("Bitmap version", 4)
    trace_write("Bitmap count", 4)
    
    # rmap section
    trace_write("rmap tag", 4, "rmap")
    trace_write("rmap unknown", 4)
    
    # Reserved entries
    bitmap_count = len(bitmap_data_list)
    trace_write(f"Reserved entries ({bitmap_count} entries)", bitmap_count * 4)
    
    # Individual bitmap data
    for i, bitmap in enumerate(bitmap_data_list):
        trace_write(f"Bitmap {i} PBMP tag", 4, "PBMP")
        trace_write(f"Bitmap {i} unknown", 4)
        trace_write(f"Bitmap {i} head", 4)
        trace_write(f"Bitmap {i} chunks", 4)
        trace_write(f"Bitmap {i} version", 4)
        trace_write(f"Bitmap {i} width", 4)
        trace_write(f"Bitmap {i} height", 4)
        trace_write(f"Bitmap {i} bitCount", 4)
        trace_write(f"Bitmap {i} flags", 4)
        trace_write(f"Bitmap {i} data tag", 4, "data")
        
        # Bitmap pixel data
        data_size = len(bitmap['data'])
        trace_write(f"Bitmap {i} pixel data", data_size)
        
        trace_write(f"Bitmap {i} padding", 4)
        trace_write(f"Bitmap {i} DETL tag", 4, "DETL")
        trace_write(f"Bitmap {i} mipmap count", 4)
        trace_write(f"Bitmap {i} final padding", 4)
    
    # Palette
    trace_write("Has palette", 4)
    
    print(f"\nTotal expected file size: 0x{current_pos:X} ({current_pos} bytes)")

if __name__ == "__main__":
    debug_font_creation("font/console_metadata.json", "bitmaps")