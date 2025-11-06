#!/usr/bin/env python3
"""
Parser for King's Quest 8 font files (.pft)
Based on the format specification from kq8pfon.txt
"""

import struct
import sys
import os
import json
from PIL import Image

# Import the conversion function from our BMP to PNG converter
try:
    from convert_bmp_to_png import convert_bmp_to_png, load_palette_from_file
    CONVERTER_AVAILABLE = True
except ImportError:
    CONVERTER_AVAILABLE = False
    print("Warning: convert_bmp_to_png module not found. PNG conversion will be skipped.")

def parse_font_file(filename, bitmaps_folder):
    """
    Parse a KQ8 font file and display all values except bitmap arrays and palette
    
    Args:
        filename: Path to the .pft font file
        bitmaps_folder: Directory to save extracted bitmap files
    """
    with open(filename, 'rb') as f:
        print(f"Parsing font file: {filename}")
        print(f"File size: {os.path.getsize(filename)} bytes")
        print("=" * 60)
        
        # Read Persistent::Base header
        block_tag = f.read(4).decode('ascii')
        print(f"Block Tag: '{block_tag}'")
        
        # Read blockSize and blockAlign (packed in 32 bits)
        block_data = struct.unpack('<I', f.read(4))[0]
        block_size = block_data & 0x7FFFFFFF  # Lower 31 bits
        block_align = (block_data >> 31) & 1  # Top bit
        print(f"Block Size: {block_size}")
        print(f"Block Align: {block_align}")
        
        # Calculate aligned size
        aligned_size = ((block_size + ((2 << block_align) - 1)) // (2 << block_align)) * (2 << block_align)
        print(f"Aligned Size: {aligned_size}")
        print()
        
        # Read Persistent::VersionedBase
        class_version = struct.unpack('<I', f.read(4))[0]
        print(f"Class Version: {class_version}")
        print()
        
        # Read GFXFont::FontInfo structure
        print("FontInfo:")
        print("-" * 40)
        
        font_flags = struct.unpack('<I', f.read(4))[0]
        print(f"Font Flags: 0x{font_flags:08X}")
        
        # Decode font flags
        flags_desc = []
        if font_flags & 0x00000001:
            flags_desc.append("proportional")
        if font_flags & 0x00000002:
            flags_desc.append("monospaced")
        if font_flags & 0x00000004:
            flags_desc.append("monochrome")
        if font_flags & 0x00000200:
            flags_desc.append("UCS-2 text")
        print(f"  Flags: {', '.join(flags_desc) if flags_desc else 'none'}")
        
        text_flags = struct.unpack('<I', f.read(4))[0]
        print(f"Text Flags: 0x{text_flags:08X}")
        
        # Decode text flags
        align_h = text_flags & 0x00000007
        align_v = text_flags & 0x00000038
        stretch = text_flags & 0x00000040
        
        h_align = "left"
        if align_h == 0x02:
            h_align = "right"
        elif align_h == 0x04:
            h_align = "center"
            
        v_align = "top"
        if align_v == 0x08:
            v_align = "bottom"
        elif align_v == 0x20:
            v_align = "center"
            
        print(f"  Horizontal Align: {h_align}")
        print(f"  Vertical Align: {v_align}")
        print(f"  Stretch: {'yes' if stretch else 'no'}")
        
        glyph_count = struct.unpack('<i', f.read(4))[0]
        char_height = struct.unpack('<i', f.read(4))[0]
        char_width = struct.unpack('<i', f.read(4))[0]
        text_color = struct.unpack('<I', f.read(4))[0]
        back_color = struct.unpack('<I', f.read(4))[0]
        baseline = struct.unpack('<i', f.read(4))[0]
        text_h_scale = struct.unpack('<I', f.read(4))[0]  # fp1616_t
        text_v_scale = struct.unpack('<I', f.read(4))[0]  # fp1616_t
        char_h_space = struct.unpack('<i', f.read(4))[0]
        
        print(f"Glyph Count: {glyph_count}")
        print(f"Char Height: {char_height}")
        print(f"Char Width: {char_width}")
        print(f"Text Color: 0x{text_color:08X}")
        print(f"Back Color: 0x{back_color:08X}")
        print(f"Baseline: {baseline}")
        print(f"Text H Scale: 0x{text_h_scale:08X} ({text_h_scale / 65536.0:.2f})")
        print(f"Text V Scale: 0x{text_v_scale:08X} ({text_v_scale / 65536.0:.2f})")
        print(f"Char H Space: {char_h_space}")
        print()
        
        # Read character mapping
        char_count = struct.unpack('<h', f.read(2))[0]
        char_first = struct.unpack('<h', f.read(2))[0]
        
        print("Character Mapping:")
        print("-" * 40)
        print(f"Char Count: {char_count}")
        print(f"First Char: {char_first} ('{chr(char_first)}' if printable)")
        
        # Read character glyph mapping array
        char_glyph = []
        for i in range(char_count):
            glyph_index = struct.unpack('<h', f.read(2))[0]
            char_glyph.append(glyph_index)
        
        print(f"Character to Glyph Mapping ({char_count} entries):")
        
        # Show characters that have actual glyphs (not -1)
        mapped_chars = []
        for i in range(char_count):
            char_code = char_first + i
            glyph_idx = char_glyph[i]
            if glyph_idx != -1:
                mapped_chars.append((char_code, glyph_idx))
        
        print(f"Characters with glyphs ({len(mapped_chars)} out of {char_count}):")
        for char_code, glyph_idx in mapped_chars:
            char_repr = repr(chr(char_code)) if 32 <= char_code <= 126 else f"\\x{char_code:02x}"
            print(f"  Char {char_code} ({char_repr}): glyph {glyph_idx}")
        
        if len(mapped_chars) == 0:
            print("  No characters have assigned glyphs!")
        print()
        
        # Read glyph info array
        print("Glyph Information:")
        print("-" * 40)
        print(f"Glyph Array ({glyph_count} entries):")
        
        glyph_array = []
        for i in range(glyph_count):
            glyph_bytes = f.read(8)  # Read all 8 bytes including spare
            glyph_info = struct.unpack('<BBBBBB', glyph_bytes[:6])  # First 6 bytes
            bitmap_index, bitmap_left, bitmap_top, width, height, baseline_shift = glyph_info
            spare_bytes = glyph_bytes[6:8]  # Last 2 bytes (spare)
            
            glyph_data = {
                'bitmap_index': bitmap_index,
                'bitmap_left': bitmap_left,
                'bitmap_top': bitmap_top,
                'width': width,
                'height': height,
                'baseline_shift': baseline_shift,
                'spare_bytes': list(spare_bytes)  # Save spare bytes as list
            }
            glyph_array.append(glyph_data)
            
            if i < 10:  # Show first 10 glyphs
                print(f"  Glyph {i}: bitmap_idx={bitmap_index}, left={bitmap_left}, top={bitmap_top}, "
                      f"size={width}x{height}, baseline_shift={baseline_shift}")
        
        if glyph_count > 10:
            print(f"  ... and {glyph_count - 10} more glyphs")
        print()
        
        # Read bitmap array header
        print("Bitmap Array Header:")
        print("-" * 40)
        
        # Read the bitmap array header
        # uint32_t chunks : 24; uint32_t version: 8; (packed in first 4 bytes)
        # uint32_t bitmapCount; (next 4 bytes)
        pbma_tag = f.read(4)  # PBMA
        pbma_unknown = struct.unpack('<I', f.read(4))[0]
        pbma_head = struct.unpack('<I', f.read(4))[0]
        bitmap_header1 = struct.unpack('<I', f.read(4))[0]  # Full 32-bit value
        chunks = bitmap_header1 & 0x00FFFFFF      # Lower 24 bits for display
        bitmap_header2 = struct.unpack('<I', f.read(4))[0]  # Full 32-bit value
        version = bitmap_header2 & 0xFF   # Lower 8 bits for display
        bitmap_count = struct.unpack('<I', f.read(4))[0]
        
        print(f"Chunks: {chunks}")
        print(f"Version: {version}")
        print(f"Bitmap Count: {bitmap_count}")
        print()
        
        # Read rmap section
        rmap_tag = f.read(4)  # rmap
        rmap_unknown = struct.unpack('<I', f.read(4))[0]
        rmap_reserved = []
        for _ in range(bitmap_count):
            reserved_value = struct.unpack('<I', f.read(4))[0]
            rmap_reserved.append(reserved_value)
        
        bitmap_headers = []
        for bitmap_index in range(bitmap_count):
            pbmp_tag = f.read(4)  # PBMP
            pbmp_unknown = struct.unpack('<I', f.read(4))[0]
            pbmp_head = struct.unpack('<I', f.read(4))[0]
            bitmap_chunks_raw = struct.unpack('<I', f.read(4))[0]
            chunks = bitmap_chunks_raw & 0x00FFFFFF      # Lower 24 bits
            bitmap_version_raw = struct.unpack('<I', f.read(4))[0]
            version = bitmap_version_raw & 0xFF   # Lower 8 bits
            width_raw = struct.unpack('<I', f.read(4))[0]
            width = ((width_raw + 3) // 4) * 4  # Aligned width for data reading
            height = struct.unpack('<I', f.read(4))[0]
            bitCount = struct.unpack('<I', f.read(4))[0]
            print(f"Chunks: {chunks}")
            print(f"Version: {version}")
            print(f"Width?: {width}")
            print(f"Height: {height}")
            print(f"Bit Count: {bitCount}")
            print()
            flags = struct.unpack('<I', f.read(4))[0]
            data_tag = f.read(4)  # 'data'
            print(f"Word: {data_tag.decode('latin1')}")
            
            # Save bitmap header data
            bitmap_header = {
                'pbmp_tag': pbmp_tag.decode('ascii'),
                'pbmp_unknown': pbmp_unknown,
                'pbmp_head': pbmp_head,
                'bitmap_chunks_raw': bitmap_chunks_raw,
                'bitmap_version_raw': bitmap_version_raw,
                'chunks': chunks,
                'version': version,
                'width_raw': width_raw,  # Original width value
                'width': width,         # Aligned width for data
                'height': height,
                'bit_count': bitCount,
                'flags': flags,
                'data_tag': data_tag.decode('latin1')
            }
            #sum=0
            
            #for index in range(4):
            #    data_size = (height * width) >> (index * 2)
            #    #Read the bitmap data
            #    f.read(data_size)
            #    sum += data_size
            #    print(f"Mipmap Level {index}: size={data_size} bytes")
            #f.read(6) #TODO - check why 6
            data_size = height * width
            
            # Read and display bitmap data
            bitmap_data = f.read(data_size)
            print(f"Bitmap Data Size: {data_size} bytes ({width}x{height})")
            
            # Create bitmaps folder if it doesn't exist
            if not os.path.exists(bitmaps_folder):
                os.makedirs(bitmaps_folder)
                print(f"Created bitmaps folder: {bitmaps_folder}")

            # Save bitmap as BMP file
            if len(bitmap_data) == data_size and width > 0 and height > 0:
                # Create PIL Image from bitmap data (8-bit grayscale)
                img = Image.new('L', (width, height))
                img.putdata(bitmap_data)
                
                # Save as BMP
                bmp_filename = os.path.join(bitmaps_folder, f"bitmap_{bitmap_index:03d}.bmp")
                img.save(bmp_filename)
                print(f"Saved bitmap to: {bmp_filename}")
                
                # Convert BMP to PNG using palette (direct function call)
                if CONVERTER_AVAILABLE:
                    png_filename = os.path.join(bitmaps_folder, f"bitmap_{bitmap_index:03d}.png")
                    palette_file = "menus.pal"
                    
                    try:
                        # Load palette if available
                        palette = None
                        if os.path.exists(palette_file):
                            palette = load_palette_from_file(palette_file)
                        
                        # Convert using direct function call
                        convert_bmp_to_png(bmp_filename, png_filename, palette)
                        print(f"Converted to PNG: {png_filename}")
                        
                    except Exception as e:
                        print(f"Warning: Could not convert {bmp_filename} to PNG: {e}")
                else:
                    print("PNG conversion skipped (converter not available)")

            bitmap_footer_unknown = f.read(4)

            #print(f"Total Bitmap Data Size: {sum} (0x{sum:X}) )bytes")
            detl_tag = f.read(4)  #'DETL'
            print(f"Word: {detl_tag.decode('latin1')}")
            mipmapCount = struct.unpack('<I', f.read(4))[0]
            print(f"Mipmap Count: {mipmapCount}")
            detl_footer_unknown = f.read(4) #Jump 4 bytes
            print("======================")
            
            # Add footer data to bitmap header
            bitmap_header['bitmap_footer_unknown'] = list(bitmap_footer_unknown)
            bitmap_header['detl_tag'] = detl_tag.decode('latin1')
            bitmap_header['mipmap_count'] = mipmapCount
            bitmap_header['detl_footer_unknown'] = list(detl_footer_unknown)
            
            bitmap_headers.append(bitmap_header)

        # Check for palette
        hasPalette = struct.unpack('<I', f.read(4))[0]
        print(f"Has Palette: {hasPalette}")
        current_pos = f.tell()
        remaining_bytes = os.path.getsize(filename) - current_pos
        print(f"Current position: {current_pos} (0x{current_pos:X})")
        print(f"Remaining bytes: {remaining_bytes}")
        
        # Save font metadata for recreation
        font_metadata = {
            'header': {
                'block_tag': block_tag,
                'block_size': block_size,
                'block_align': block_align,
                'class_version': class_version
            },
            'font_info': {
                'font_flags': font_flags,
                'text_flags': text_flags,
                'glyph_count': glyph_count,
                'char_height': char_height,
                'char_width': char_width,
                'text_color': text_color,
                'back_color': back_color,
                'baseline': baseline,
                'text_h_scale': text_h_scale,
                'text_v_scale': text_v_scale,
                'char_h_space': char_h_space
            },
            'character_mapping': {
                'char_count': char_count,
                'char_first': char_first,
                'char_glyph': char_glyph
            },
            'glyph_array': glyph_array,
            'bitmap_array': {
                'pbma_tag': pbma_tag.decode('ascii'),
                'pbma_unknown': pbma_unknown,
                'pbma_head': pbma_head,
                'bitmap_header1': bitmap_header1,  # Full 32-bit value
                'bitmap_header2': bitmap_header2,  # Full 32-bit value
                'chunks': chunks,  # Decoded value for reference
                'version': version,  # Decoded value for reference
                'bitmap_count': bitmap_count,
                'rmap_tag': rmap_tag.decode('ascii'),
                'rmap_unknown': rmap_unknown,
                'rmap_reserved': rmap_reserved,
                'bitmap_headers': bitmap_headers  # Individual bitmap header data
            },
            'palette': {
                'has_palette': hasPalette
            }
        }
        
        # Save metadata to JSON file
        metadata_filename = os.path.splitext(filename)[0] + '_metadata.json'
        with open(metadata_filename, 'w') as meta_file:
            json.dump(font_metadata, meta_file, indent=2)
        print(f"Saved font metadata to: {metadata_filename}")
        

def main():
    """Main function"""
    if len(sys.argv) != 3:
        print("Usage: python parse_font.py <font_file.pft> <bitmaps_folder>")
        print("Examples:")
        print("  python parse_font.py font/14.pft bitmaps")
        print("  python parse_font.py font/14.pft extracted_bitmaps")
        print("  python parse_font.py C:\\Games\\KQ8\\font\\console.pft C:\\Output\\FontBitmaps")
        sys.exit(1)
    
    font_file = sys.argv[1]
    bitmaps_folder = sys.argv[2]
    
    # Check if file exists
    if not os.path.exists(font_file):
        print(f"Error: Font file '{font_file}' not found")
        sys.exit(1)
    
    print(f"Font file: {font_file}")
    print(f"Bitmaps folder: {bitmaps_folder}")
    print()
    
    try:
        parse_font_file(font_file, bitmaps_folder)
        
    except Exception as e:
        print(f"Error parsing font file: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()