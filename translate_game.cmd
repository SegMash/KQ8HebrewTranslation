@echo off
setlocal enabledelayedexpansion
REM Translation workflow script for KQ8 Hebrew Translation
REM Loops through game locations and runs repeated commands
if not "%1"=="" if not "%2"=="" goto %1

set GAME_PATH=C:\Games\KQ8
set BACKUP_PATH=C:\Games\Backup\KQ8
set GLYPHS_FIXED=.\glyphs_fixed
set GLYPHS_FIXED_CONSOLE=.\glyphs_fixed_console_menu
set GLYPHS_FIXED_CONSOLEL=.\glyphs_fixed_consolel
set GLYPHS_FIXED_20=.\glyphs_fixed_20
set GLYPHS_FIXED_20_SL=.\glyphs_fixed_20_sl
set GLYPHS_FIXED_27=.\glyphs_fixed_27
set GLYPHS_FIXED_36=.\glyphs_fixed_36
set GLYPHS_FIXED_45=.\glyphs_fixed_45
set GLYPHS_FIXED_45_SL=.\glyphs_fixed_45_sl

echo ========================================
echo KQ8 Hebrew Translation Workflow
echo ========================================
echo.

python.exe .\fix_glyph.py .\glyphs_8 %GLYPHS_FIXED%
python.exe .\fix_glyph.py .\glyphs_16_15_menu %GLYPHS_FIXED_CONSOLE%
python.exe .\fix_glyph.py .\glyphs_16_21 %GLYPHS_FIXED_20%
python.exe .\fix_glyph.py .\glyphs_16_21_sl %GLYPHS_FIXED_20_SL%
python.exe .\fix_glyph.py .\glyphs_16_21_l %GLYPHS_FIXED_CONSOLEL%
python.exe .\fix_glyph.py .\glyphs_24_38 %GLYPHS_FIXED_27%
python.exe .\fix_glyph.py .\glyphs_24_38 %GLYPHS_FIXED_36%
python.exe .\fix_glyph.py .\glyphs_32_46 %GLYPHS_FIXED_45%
python.exe .\fix_glyph.py .\glyphs_32_46_sl %GLYPHS_FIXED_45_SL%

REM ========================================
REM 0. Restore Font Files from Backup
REM ========================================
echo [0/5] Restoring font files from backup...
echo.

for %%L in (daventry castled deadcity swamp gnome barren iceworld snowexit temple1 temple2 temple3 temple4) do (
    echo Copying %%L fonts...
    xcopy /Y "%BACKUP_PATH%\%%L\8gui\*.pft" "%GAME_PATH%\%%L\8gui\"
)
echo Copying GAME fonts...
xcopy /Y "%BACKUP_PATH%\GAME\8Gui\*.pft" "%GAME_PATH%\GAME\8Gui\"
echo.

REM ========================================
REM 1. Parse Font Files
REM ========================================
echo [1/5] Parsing font files...
echo.

for %%L in (daventry castled deadcity swamp gnome barren iceworld snowexit temple1 temple2 temple3 temple4) do (
    echo Processing %%L...
    python.exe .\parse_font.py %GAME_PATH%\%%L\8gui\console.pft %%L\bitmaps
)

python.exe .\parse_font.py %GAME_PATH%\GAME\8Gui\consoleg.pft .\GAME\bitmaps_consoleg
python.exe .\parse_font.py %GAME_PATH%\GAME\8Gui\consolel.pft .\GAME\bitmaps_consolel
python.exe .\parse_font.py %GAME_PATH%\GAME\8Gui\consoles.pft .\GAME\bitmaps_consoles
python.exe .\parse_font.py %GAME_PATH%\GAME\8Gui\20.pft .\GAME\bitmaps_20
python.exe .\parse_font.py %GAME_PATH%\GAME\8Gui\20sl.pft .\GAME\bitmaps_20sl
python.exe .\parse_font.py %GAME_PATH%\GAME\8Gui\27.pft .\GAME\bitmaps_27
python.exe .\parse_font.py %GAME_PATH%\GAME\8Gui\27sl.pft .\GAME\bitmaps_27sl
python.exe .\parse_font.py %GAME_PATH%\GAME\8Gui\36.pft .\GAME\bitmaps_36
python.exe .\parse_font.py %GAME_PATH%\GAME\8Gui\36sl.pft .\GAME\bitmaps_36sl
python.exe .\parse_font.py %GAME_PATH%\GAME\8Gui\45.pft .\GAME\bitmaps_45
python.exe .\parse_font.py %GAME_PATH%\GAME\8Gui\45sl.pft .\GAME\bitmaps_45sl

for %%L in (daventry castled deadcity swamp gnome barren iceworld snowexit temple1 temple2 temple3 temple4) do (
    echo Processing %%L palette...
    set "RESOURCE_DIR=%GAME_PATH%\%%L\resource"
    set "PPL_FILE="
    for %%F in ("!RESOURCE_DIR!\*.ppl") do (
        if "!PPL_FILE!"=="" set "PPL_FILE=%%F"
    )
    if not "!PPL_FILE!"=="" (
        python.exe .\parse_ppl.py "!PPL_FILE!" .\%%L\%%L.pal
        python.exe .\parse_ppl.py visualize .\%%L\%%L.pal .\%%L\%%L_palette.png
    ) else (
        echo Warning: No PPL file found in !RESOURCE_DIR!
    )
)
echo.
echo Now add mapping to colors in png_to_bmp.py
rem pause

REM ========================================
REM 2. Convert PNG to BMP
REM ========================================
echo [2/5] Converting PNG to BMP...
echo.

for %%L in (daventry castled deadcity swamp gnome barren iceworld snowexit temple1 temple2 temple3 temple4) do (
    echo Processing %%L...
    python png_to_bmp.py %GLYPHS_FIXED_CONSOLE% %%L .\%%L\bitmaps
)
python.exe .\png_to_bmp.py %GLYPHS_FIXED_CONSOLE% console .\GAME\bitmaps_consoleg
python.exe .\png_to_bmp.py %GLYPHS_FIXED_CONSOLE% consoles .\GAME\bitmaps_consoles
python.exe .\png_to_bmp.py %GLYPHS_FIXED_CONSOLEL% consolel .\GAME\bitmaps_consolel
python.exe .\png_to_bmp.py %GLYPHS_FIXED_20% 20 .\GAME\bitmaps_20
python.exe .\png_to_bmp.py %GLYPHS_FIXED_20_SL% 20sl .\GAME\bitmaps_20sl
python.exe .\png_to_bmp.py %GLYPHS_FIXED_27% 27 .\GAME\bitmaps_27
python.exe .\png_to_bmp.py %GLYPHS_FIXED_27% 27sl .\GAME\bitmaps_27sl
python.exe .\png_to_bmp.py %GLYPHS_FIXED_36% 36 .\GAME\bitmaps_36
python.exe .\png_to_bmp.py %GLYPHS_FIXED_36% 36sl .\GAME\bitmaps_36sl
python.exe .\png_to_bmp.py %GLYPHS_FIXED_45% 45 .\GAME\bitmaps_45
python.exe .\png_to_bmp.py %GLYPHS_FIXED_45_SL% 45sl .\GAME\bitmaps_45sl
echo.

REM ========================================
REM 3. Create Font Files
REM ========================================
echo [3/5] Creating font files...
echo.

for %%L in (daventry castled deadcity swamp gnome barren iceworld snowexit temple1 temple2 temple3 temple4) do (
    echo Processing %%L...
    python.exe .\create_font.py %GAME_PATH%\%%L\8gui\console_metadata.json .\%%L\bitmaps %GAME_PATH%\%%L\8gui\console.pft
)
python.exe .\create_font.py %GAME_PATH%\GAME\8Gui\consoleg_metadata.json .\GAME\bitmaps_consoleg %GAME_PATH%\GAME\8Gui\consoleg.pft
python.exe .\create_font.py %GAME_PATH%\GAME\8Gui\consoleg_metadata.json .\GAME\bitmaps_consoles %GAME_PATH%\GAME\8Gui\consoles.pft
python.exe .\create_font.py %GAME_PATH%\GAME\8Gui\consolel_metadata.json .\GAME\bitmaps_consolel %GAME_PATH%\GAME\8Gui\consolel.pft
python.exe .\create_font.py %GAME_PATH%\GAME\8Gui\20_metadata.json .\GAME\bitmaps_20 %GAME_PATH%\GAME\8Gui\20.pft
python.exe .\create_font.py %GAME_PATH%\GAME\8Gui\20sl_metadata.json .\GAME\bitmaps_20sl %GAME_PATH%\GAME\8Gui\20sl.pft
python.exe .\create_font.py %GAME_PATH%\GAME\8Gui\27_metadata.json .\GAME\bitmaps_27 %GAME_PATH%\GAME\8Gui\27.pft
python.exe .\create_font.py %GAME_PATH%\GAME\8Gui\27sl_metadata.json .\GAME\bitmaps_27sl %GAME_PATH%\GAME\8Gui\27sl.pft
python.exe .\create_font.py %GAME_PATH%\GAME\8Gui\36_metadata.json .\GAME\bitmaps_36 %GAME_PATH%\GAME\8Gui\36.pft
python.exe .\create_font.py %GAME_PATH%\GAME\8Gui\36sl_metadata.json .\GAME\bitmaps_36sl %GAME_PATH%\GAME\8Gui\36sl.pft
python.exe .\create_font.py %GAME_PATH%\GAME\8Gui\45_metadata.json .\GAME\bitmaps_45 %GAME_PATH%\GAME\8Gui\45.pft
python.exe .\create_font.py %GAME_PATH%\GAME\8Gui\45sl_metadata.json .\GAME\bitmaps_45sl %GAME_PATH%\GAME\8Gui\45sl.pft
echo.

REM ========================================
REM 4. Parse MSG Files
REM ========================================
echo [4/5] Parsing MSG files...
echo.

REM daventry -> 1000, deadcity -> 2000, swamp -> 3000
call :parse_msg_csv GAME 0
call :parse_msg_csv GAME 500
call :parse_msg_csv daventry 1000
call :parse_msg_csv deadcity 2000
call :parse_msg_csv swamp 3000
call :parse_msg_csv gnome 4000
call :parse_msg_csv barren 5000
call :parse_msg_csv iceworld 6000
call :parse_msg_csv temple1 7000
REM Fix lines break
python.exe .\fix_csv_linebreaks.py GAME\500_messages.csv
echo.

REM ========================================
REM 5. Process Messages
REM ========================================
echo [5/5] Processing messages...
echo.
call :process_csv_to_english_txt GAME 0
call :process_csv_to_english_txt GAME 500
call :process_csv_to_english_txt daventry 1000
call :process_csv_to_english_txt deadcity 2000
call :process_csv_to_english_txt swamp 3000
call :process_csv_to_english_txt gnome 4000
call :process_csv_to_english_txt barren 5000
call :process_csv_to_english_txt iceworld 6000
call :process_csv_to_english_txt temple1 7000
echo.

echo Verify the english and hebrew txt files are alligned and correct.
rem pause

REM ========================================
REM 6. Translate MSG files
REM ========================================
echo [6/6] Translating MSG files...
echo.
call :hebrew_txt_to_MSG GAME 0
call :hebrew_txt_to_MSG GAME 500
call :hebrew_txt_to_MSG daventry 1000
call :hebrew_txt_to_MSG deadcity 2000
call :hebrew_txt_to_MSG swamp 3000
call :hebrew_txt_to_MSG gnome 4000
call :hebrew_txt_to_MSG barren 5000
call :hebrew_txt_to_MSG iceworld 6000
call :hebrew_txt_to_MSG temple1 7000
echo.

REM ========================================
REM 7. End
REM ========================================
echo [7/7] Ending...
echo.

goto :end

:parse_msg_csv
echo Processing %1 (MSG %2)...
echo Copying MSG file from backup...
xcopy /Y "%BACKUP_PATH%\%1\English\%2.MSG" "%GAME_PATH%\%1\English\"
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
if "%2"=="7000" (
    echo Running additional command for temple2...
    python create_msg.py %1\%2_messages_hebrew.csv %GAME_PATH%\temple2\English\%2%.MSG
)

goto :eof
:end

echo ========================================
echo Workflow completed!
echo ========================================
rem pause

