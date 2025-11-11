@echo off
setlocal enabledelayedexpansion
REM Translation workflow script for KQ8 Hebrew Translation
REM Loops through game locations and runs repeated commands

set GAME_PATH=C:\Games\KQ8
set GLYPHS_FIXED=.\glyphs_fixed

echo ========================================
echo KQ8 Hebrew Translation Workflow
echo ========================================
echo.

python.exe .\fix_glyph.py .\glyphs %GLYPHS_FIXED%
REM ========================================
REM 1. Parse Font Files
REM ========================================
echo [1/5] Parsing font files...
echo.

for %%L in (daventry castled deadcity swamp gnome) do (
    echo Processing %%L...
    python.exe .\parse_font.py %GAME_PATH%\%%L\8gui\console.pft %%L\bitmaps
)
echo.
echo Now add mapping to colors in png_to_bmp.py
rem pause

REM ========================================
REM 2. Convert PNG to BMP
REM ========================================
echo [2/5] Converting PNG to BMP...
echo.

for %%L in (daventry castled deadcity swamp gnome) do (
    echo Processing %%L...
    python png_to_bmp.py %GLYPHS_FIXED% %%L .\%%L\bitmaps
)
echo.

REM ========================================
REM 3. Create Font Files
REM ========================================
echo [3/5] Creating font files...
echo.

for %%L in (daventry castled deadcity swamp gnome) do (
    echo Processing %%L...
    python.exe .\create_font.py %GAME_PATH%\%%L\8gui\console_metadata.json .\%%L\bitmaps %GAME_PATH%\%%L\8gui\console.pft
)
echo.

REM ========================================
REM 4. Parse MSG Files
REM ========================================
echo [4/5] Parsing MSG files...
echo.

REM daventry -> 1000, deadcity -> 2000, swamp -> 3000
call :parse_msg_csv daventry 1000
call :parse_msg_csv deadcity 2000
call :parse_msg_csv swamp 3000
call :parse_msg_csv gnome 4000
echo.

REM ========================================
REM 5. Process Messages
REM ========================================
echo [5/5] Processing messages...
echo.

call :process_csv_to_english_txt daventry 1000
call :process_csv_to_english_txt deadcity 2000
call :process_csv_to_english_txt swamp 3000
call :process_csv_to_english_txt gnome 4000
echo.

echo Verify the english and hebrew txt files are alligned and correct.
rem pause

REM ========================================
REM 6. Translate MSG files
REM ========================================
echo [6/6] Translating MSG files...
echo.
call :hebrew_txt_to_MSG GAME 0
call :hebrew_txt_to_MSG daventry 1000
call :hebrew_txt_to_MSG deadcity 2000
call :hebrew_txt_to_MSG swamp 3000
call :hebrew_txt_to_MSG gnome 4000
echo.

REM ========================================
REM 7. End
REM ========================================
echo [7/7] Ending...
echo.

goto :end

:parse_msg_csv
echo Processing %1 (MSG %2)...
python.exe .\parse_msg.py %GAME_PATH%\%1\English\%2.MSG %1
goto :eof

:process_csv_to_english_txt
echo Processing %1 (MSG %2)...
python process_messages.py %1\%2_messages.csv %1
goto :eof


:hebrew_txt_to_MSG
echo Processing %1 (MSG %2)...
python map_files.py %1\%2_messages_english.txt %1\%2_messages_hebrew.txt %1\%2_mapping.txt 26
python translate_csv.py %1\%2_messages.csv %1\%2_mapping.txt %1\%2_messages_hebrew.csv
python create_msg.py %1\%2_messages_hebrew.csv %GAME_PATH%\%1\English\%2.MSG

goto :eof
:end

echo ========================================
echo Workflow completed!
echo ========================================
rem pause

