#!/usr/bin/env python3
"""
Creator for King's Quest 8 font files (.pft)
Creates font file from saved metadata and bitmap BMP files
"""

import struct
import sys
import os
import json
import glob
from PIL import Image

def create_font_file(metadata_filename, bitmaps_folder, output_filename):
    """
    Create a KQ8 font file from metadata and bitmap BMPs
    
    Args:
        metadata_filename: Path to the JSON metadata file
        bitmaps_folder: Path to folder containing bitmap BMP files
        output_filename: Path to output font file
    """
    
    # Load metadata
    with open(metadata_filename, 'r') as meta_file:
        metadata = json.load(meta_file)
    
    print(f"Loaded metadata from: {metadata_filename}")

    # Scan bitmaps folder for BMP files
    bitmap_files = glob.glob(os.path.join(bitmaps_folder, "bitmap_*.bmp"))
    bitmap_files.sort()  # Sort to ensure consistent order
    
    # Extract bitmap indices from filenames and create mapping
    bitmap_data_list = []
    for bitmap_file in bitmap_files:
        filename = os.path.basename(bitmap_file)
        # Extract index from "bitmap_XXX.bmp"
        if filename.startswith("bitmap_") and filename.endswith(".bmp"):
            index_str = filename[7:-4]  # Remove "bitmap_" and ".bmp"
            try:
                index = int(index_str)
                
                # Load bitmap image
                img = Image.open(bitmap_file)
                if img.mode != 'L':
                    img = img.convert('L')  # Convert to grayscale if needed
                
                bitmap_data = {
                    'index': index,
                    'width': img.width,
                    'height': img.height,
                    'data': list(img.getdata())  # Get pixel data as list
                }
                bitmap_data_list.append(bitmap_data)
                print(f"Loaded bitmap {index}: {img.width}x{img.height} from {bitmap_file}")
                
            except ValueError:
                print(f"Warning: Skipping invalid bitmap filename: {filename}")
    
    # Sort bitmaps by index
    bitmap_data_list.sort(key=lambda x: x['index'])
    
    print(f"Found {len(bitmap_data_list)} bitmap files")
    
    # Update bitmap count in metadata
    metadata['bitmap_array']['bitmap_count'] = len(bitmap_data_list)
    
    # Write font file
    with open(output_filename, 'wb') as f:
        # Write Persistent::Base header
        f.write(metadata['header']['block_tag'].encode('ascii'))
        
        # Calculate actual block size (file size - 8 bytes for header)
        # We'll write a placeholder for now and update it at the end
        block_size_pos = f.tell()
        f.write(struct.pack('<I', 0))  # Placeholder for block_size
        
        # Write Persistent::VersionedBase
        f.write(struct.pack('<I', metadata['header']['class_version']))
        
        # Write GFXFont::FontInfo structure
        f.write(struct.pack('<I', metadata['font_info']['font_flags']))
        f.write(struct.pack('<I', metadata['font_info']['text_flags']))
        f.write(struct.pack('<i', metadata['font_info']['glyph_count']))
        f.write(struct.pack('<i', metadata['font_info']['char_height']))
        f.write(struct.pack('<i', metadata['font_info']['char_width']))
        f.write(struct.pack('<I', metadata['font_info']['text_color']))
        f.write(struct.pack('<I', metadata['font_info']['back_color']))
        f.write(struct.pack('<i', metadata['font_info']['baseline']))
        f.write(struct.pack('<I', metadata['font_info']['text_h_scale']))
        f.write(struct.pack('<I', metadata['font_info']['text_v_scale']))
        f.write(struct.pack('<i', metadata['font_info']['char_h_space']))
        
        # Write character mapping
        f.write(struct.pack('<h', metadata['character_mapping']['char_count']))
        f.write(struct.pack('<h', metadata['character_mapping']['char_first']))
        
        # Write character glyph mapping array
        for glyph_index in metadata['character_mapping']['char_glyph']:
            f.write(struct.pack('<h', glyph_index))
        
        # Write glyph info array
        for i, glyph in enumerate(metadata['glyph_array']):
            # Find corresponding bitmap to get actual width
            bitmap_index = glyph['bitmap_index']
            actual_width = glyph['width']  # Default to metadata width
            
            # Look for bitmap with matching index
            for bitmap in bitmap_data_list:
                if bitmap['index'] == bitmap_index:
                    actual_width = bitmap['width']  # Use actual bitmap width
                    break
            #if bitmap_index==107:
            #    actual_width = 12
                
            
            # Write the main 6 bytes (using actual bitmap width)
            f.write(struct.pack('<BBBBBB', 
                               glyph['bitmap_index'],
                               glyph['bitmap_left'],
                               glyph['bitmap_top'],
                               actual_width,  # Use actual bitmap width instead of metadata
                               glyph['height'],
                               glyph['baseline_shift']))
            
            # Write the spare bytes (if available, otherwise write zeros)
            if 'spare_bytes' in glyph and len(glyph['spare_bytes']) == 2:
                f.write(bytes(glyph['spare_bytes']))
            else:
                f.write(b'\x00\x00')  # Default spare bytes
        
        # Write bitmap array header
        f.write(metadata['bitmap_array']['pbma_tag'].encode('ascii'))  # Tag
        f.write(struct.pack('<I', metadata['bitmap_array']['pbma_unknown']))  # Unknown
        f.write(struct.pack('<I', metadata['bitmap_array']['pbma_head']))  # Head
        
        # Write bitmap header with full 32-bit values
        f.write(struct.pack('<I', metadata['bitmap_array']['bitmap_header1']))
        f.write(struct.pack('<I', metadata['bitmap_array']['bitmap_header2']))
        
        # Write bitmap count
        f.write(struct.pack('<I', len(bitmap_data_list)))
        
        # Write rmap section
        f.write(metadata['bitmap_array']['rmap_tag'].encode('ascii'))  # Tag
        f.write(struct.pack('<I', metadata['bitmap_array']['rmap_unknown']))  # Unknown
        
        # Write reserved entries for each bitmap
        original_reserved = metadata['bitmap_array']['rmap_reserved']
        for i in range(len(bitmap_data_list)):
            if i < len(original_reserved):
                f.write(struct.pack('<I', original_reserved[i]))  # Original reserved value
            else:
                f.write(struct.pack('<I', 0))  # Default for new bitmaps
        
        # Write bitmap data
        bitmap_headers = metadata['bitmap_array'].get('bitmap_headers', [])
        for i, bitmap in enumerate(bitmap_data_list):
            # Use saved header data if available, otherwise use defaults
            if i < len(bitmap_headers):
                header = bitmap_headers[i]
                # Write PBMP header with saved values
                f.write(header['pbmp_tag'].encode('ascii'))
                f.write(struct.pack('<I', header['pbmp_unknown']))
                f.write(struct.pack('<I', header['pbmp_head']))
                
                # Write bitmap info with saved raw values
                f.write(struct.pack('<I', header['bitmap_chunks_raw']))
                f.write(struct.pack('<I', header['bitmap_version_raw']))
                width = bitmap['width']
                f.write(struct.pack('<I', width))  # Use calculated width
                f.write(struct.pack('<I', header['height']))
                f.write(struct.pack('<I', header['bit_count']))
                
                # Write flags and data tag with saved values
                f.write(struct.pack('<I', header['flags']))
                f.write(header['data_tag'].encode('ascii'))
            else:
                # Fallback to defaults for new bitmaps
                f.write(b'PBMP')
                f.write(struct.pack('<I', 0))
                f.write(struct.pack('<I', 0))
                
                chunks = metadata['bitmap_array']['chunks'] & 0x00FFFFFF
                f.write(struct.pack('<I', chunks))
                version = metadata['bitmap_array']['version'] & 0xFF
                f.write(struct.pack('<I', version))
                
                width = ((bitmap['width'] + 3) // 4) * 4
                f.write(struct.pack('<I', width))
                f.write(struct.pack('<I', bitmap['height']))
                f.write(struct.pack('<I', 8))
                f.write(struct.pack('<I', 0))
                f.write(b'data')
            
            # Write bitmap data
            bitmap_bytes = bytes(bitmap['data'])
            f.write(bitmap_bytes)
            
            # Write footer with saved values
            if i < len(bitmap_headers):
                header = bitmap_headers[i]
                f.write(bytes(header['bitmap_footer_unknown']))
                f.write(header['detl_tag'].encode('ascii'))
                f.write(struct.pack('<I', header['mipmap_count']))
                f.write(bytes(header['detl_footer_unknown']))
            else:
                # Fallback to defaults
                f.write(struct.pack('<I', 0))
                f.write(b'DETL')
                f.write(struct.pack('<I', 4))
                f.write(struct.pack('<I', 0))
        
        # Write palette info
        f.write(struct.pack('<I', metadata['palette']['has_palette']))
        
        # Now calculate the actual file size and update the block_size
        current_pos = f.tell()
        actual_block_size = current_pos - 8  # File size minus 8 bytes for header
        
        # Go back and write the correct block_size
        f.seek(block_size_pos)
        block_data = (actual_block_size & 0x7FFFFFFF) | \
                    ((metadata['header']['block_align'] & 1) << 31)
        f.write(struct.pack('<I', block_data))
        
        # Return to end of file
        f.seek(current_pos)
    
    print(f"Created font file: {output_filename}")
    print(f"File size: {os.path.getsize(output_filename)} bytes")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python create_font.py <metadata_json> [bitmaps_folder] [output_font]")
        print("Example: python create_font.py console_metadata.json bitmaps console_new.pft")
        sys.exit(1)
    
    metadata_file = sys.argv[1]
    
    if len(sys.argv) >= 3:
        bitmaps_folder = sys.argv[2]
    else:
        bitmaps_folder = "bitmaps"
    
    if len(sys.argv) >= 4:
        output_font = sys.argv[3]
    else:
        # Generate output filename from metadata file
        base_name = os.path.splitext(metadata_file)[0]
        if base_name.endswith('_metadata'):
            base_name = base_name[:-9]  # Remove '_metadata'
        output_font = f"{base_name}_new.pft"
    
    # Check if files exist
    if not os.path.exists(metadata_file):
        print(f"Error: Metadata file '{metadata_file}' not found")
        sys.exit(1)
    
    if not os.path.exists(bitmaps_folder):
        print(f"Error: Bitmaps folder '{bitmaps_folder}' not found")
        sys.exit(1)
    
    try:
        print(f"Creating font file from {metadata_file} and {bitmaps_folder}...")
        create_font_file(metadata_file, bitmaps_folder, output_font)
        
        print(f"\nSUCCESS: Font file created: {output_font}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()