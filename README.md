# Font Creation
First find the palette:
- `python.exe .\parse_ppl.py C:\Games\KQ8\GAME\8Gui\Menus.ppl .\menus.pal`
Create current bitmap file. for example the subtitle font:
- `python.exe .\parse_font.py C:\Games\KQ8\daventry\8gui\console.pft bitmaps`
- `python.exe .\parse_font.py C:\Games\KQ8\castled\8gui\console.pft castle\bitmaps`
- `python.exe .\parse_font.py C:\Games\KQ8\deadcity\8gui\console.pft deadcity\bitmaps`
- `python.exe .\parse_font.py C:\Games\KQ8\swamp\8gui\console.pft swamp\bitmaps`
Now understand the colors of the bitmaps
`python.exe .\debug_bitmap.py .\deadcity\bitmaps\bitmap_065.bmp`
And then update png_to_bmp.py with the new colors
(this script uses the convert_bmp_to_png script)
Now work on the letters 096-122 and convert back to bmp
If you need to fix more letters (like ! -001 - this is the time. save it in glyphs directory as color png)
Script to fix glyphs to prepare a font
`python.exe .\fix_glyph.py .\glyphs_12 .\glyphs_fixed`

Convert back to bmp and save them in bitmaps folder:
- `python png_to_bmp.py .\glyphs_fixed daventry .\bitmaps`
- `python png_to_bmp.py .\glyphs_fixed castle .\castle\bitmaps`
- `python png_to_bmp.py .\glyphs_fixed deadcity .\deadcity\bitmaps`
- `python png_to_bmp.py .\glyphs_fixed swamp .\swamp\bitmaps`

And now recreate the font
- `python.exe .\create_font.py C:\Games\KQ8\daventry\8gui\console_metadata.json .\bitmaps C:\Games\KQ8\daventry\8gui\console.pft`
- `python.exe .\create_font.py C:\Games\KQ8\castled\8gui\console_metadata.json .\castle\bitmaps C:\Games\KQ8\castled\8gui\console.pft`
- `python.exe .\create_font.py C:\Games\KQ8\deadcity\8gui\console_metadata.json .\deadcity\bitmaps C:\Games\KQ8\deadcity\8gui\console.pft`
- `python.exe .\create_font.py C:\Games\KQ8\swamp\8gui\console_metadata.json .\swamp\bitmaps C:\Games\KQ8\swamp\8gui\console.pft`

# Translation process
1. parse the MSG file
`python.exe .\parse_msg.py C:\Games\KQ8\daventry\English\1000.MSG daventry`
`python.exe .\parse_msg.py C:\Games\KQ8\deadcity\English\2000.MSG deadcity`
`python.exe .\parse_msg.py C:\Games\KQ8\swamp\English\3000.MSG swamp`

2. extract english messages
`python process_messages.py daventry/1000_messages.csv daventry`
`python process_messages.py deadcity/2000_messages.csv deadcity`
`python process_messages.py swamp/3000_messages.csv swamp`
3. AI - Translate to hebrew - use `translate_promopt.txt` - agent should create output\1000_messages_output_hebrew.txt
4. Check files are alligned (1000_messages_output.txt & 1000_messages_output_hebrew.txt)
5. Create mapping file.
6. Create new csv file.
7. Create msg file.
`example: .\recreate_msg.cmd`

# More trnaslations tools
1. create_csv.py - get english & hebrew files and create csv with tested?, comments columns.
`python create_csv.py output/1000_messages_output.txt output/1000_messages_output_hebrew.txt output/1000_translations.csv`
2. Upload to google drive:
`python csv_xlsx_drive_v3.py --upload output\1000_translations.csv --title "KQ8 - Daventry"`
3. Show all uploaded files and their ids
`csv_xlsx_drive_v3.py --list`
4. Delete an old file
`python csv_xlsx_drive_v3.py --delete 1Euo9A-NLGVUW2PK8QZEm6TJUc4BXmdcA`
5. Download a file
6. ex: `python csv_xlsx_drive_v3.py --download --file-id 1rt-X4_xEyGppNUYap5uc28vAdPAfCvP_ --output output\1000_translations_new.csv`


# More bitmap tools
1. Show bitmap pixels:
`python.exe .\debug_bitmap.py .\castle\bitmaps\bitmap_065.bmp`


# KQ8 MSG File Parser

This project contains a Python script to parse King's Quest 8 MSG files and export them to CSV format.

## Files

- `parse_msg.py` - Main parser script
- `1000_messages.csv` - Exported messages from 1000.MSG file
- `text/1000.MSG` - Original MSG file

## CSV Column Meanings

The exported CSV file contains the following columns based on the MSG file structure:

| Column | Type | Description |
|--------|------|-------------|
| `noun` | uint8 | Noun identifier |
| `verb` | uint8 | Verb identifier (see game/english/verbs.sh) |
| `case` | uint8 | Case identifier |
| `sequence` | uint8 | Sequence number |
| `talker` | uint8 | Talker identifier (see game/english/talkers.sh) |
| `text_offset` | uint16 | Offset to text data (relative to resData) |
| `ref_noun` | uint8 | Reference noun (not used by KQMoE) |
| `ref_verb` | uint8 | Reference verb (not used by KQMoE) |
| `ref_case` | uint8 | Reference case (not used by KQMoE) |
| `ref_sequence` | uint8 | Reference sequence (not used by KQMoE) |
| `text` | string | The actual message text |

## MSG File Format

Based on the KQ8 documentation at: https://svn.nicode.net/libkq8fpc/doc/kq8msg.txt

The MSG file structure is:
1. 2-byte header (ignored)
2. 4-byte sciVersion (ignored)
3. 2-byte dataSize (important)
4. 2-byte lastId
5. 2-byte count (number of messages)
6. Loop of `count` message headers (10 bytes each)
7. Loop of `count` null-terminated text strings
8. Loop of `count` developer comments (ignored)

## Usage

```bash
python parse_msg.py
```

The script will:
1. Parse `text/1000.MSG`
2. Extract all message data
3. Export to `1000_messages.csv`

## Text Processing Notes

- Text in parentheses is stripped in the original game
- Parenthetical blocks might include `#` or numbers in square brackets
- `#` enables KQTalk.nostop
- Numbers set camera position (see KQConvInfo objects)
- Example: `"([#5] foo ) text (bar) 17 "` becomes `" text 17 "`

## Character Encoding

The script attempts to decode text using:
1. Windows-1252 (primary)
2. UTF-8 (fallback)
3. Latin1 (final fallback)

## Summerize of all fonts
1. Game/consolel(16X21) FRNEW - loading screen text  #colors: #236,238,241,186,188 (shadow=10)
2. Game/20sl(16X21) -FRNEW Load/Save menu buttons #127,124,194,125,192 (shadow=25) 
3. Game/45sl(32X46) FRNEW - Load/Save screen title #127,124,199,197,195,192,125,110,88,(25?) (shadow=58)
4. Game/45(32X46)-FRNEW-Title Options screen   #14,17,16,21,114,115,116,159,153,136,137,138,139 (shadow=46)
5. Game/36(32X38)-FRNEW- Menu & Options #11,13,15,119,116,159,153,154,136,135,26,29,39,24 (shadow=46)
6. Game/27(32X38)-FRNEW- Menu & Options  #11,13,15,119,116,159,153,154,136,135,26,29,39,24 (shadow=46)
7. Game/20(16X21)-FRNEW- Menu small items #14,17,16,21,114,115,116,159,153,136,137,138,139 (shadow=46)
8. Game/consoleg(12X15) - menu questions 123,124,122,119,154,159 shadow=209
9. console


