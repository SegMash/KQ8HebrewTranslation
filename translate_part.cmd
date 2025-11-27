@echo off
REM Translate a specific part and MSG file
REM Usage: translate_part.cmd <part_name> <msg_prefix> <max_line_length>
REM Example: translate_part.cmd GAME 0 28
REM Example: translate_part.cmd daventry 1000 26

if "%1"=="" (
    echo Error: Part name is required
    echo Usage: translate_part.cmd ^<part_name^> ^<msg_prefix^> ^<max_line_length^>
    echo Example: translate_part.cmd GAME 0 28
    exit /b 1
)

if "%2"=="" (
    echo Error: MSG prefix is required
    echo Usage: translate_part.cmd ^<part_name^> ^<msg_prefix^> ^<max_line_length^>
    echo Example: translate_part.cmd daventry 1000 26
    exit /b 1
)

if "%3"=="" (
    echo Error: Max line length is required
    echo Usage: translate_part.cmd ^<part_name^> ^<msg_prefix^> ^<max_line_length^>
    echo Example: translate_part.cmd GAME 0 28
    exit /b 1
)

set PART_NAME=%1
set MSG_PREFIX=%2
set MAX_LINE_LENGTH=%3
set GAME_PATH=C:\Games\KQ8

echo Processing %PART_NAME% (MSG %MSG_PREFIX%) with max line length %MAX_LINE_LENGTH%...
python map_files.py %PART_NAME%\%MSG_PREFIX%_messages_english.txt %PART_NAME%\%MSG_PREFIX%_messages_hebrew.txt %PART_NAME%\%MSG_PREFIX%_mapping.txt %MAX_LINE_LENGTH%
python translate_csv.py %PART_NAME%\%MSG_PREFIX%_messages.csv %PART_NAME%\%MSG_PREFIX%_mapping.txt %PART_NAME%\%MSG_PREFIX%_messages_hebrew.csv
python create_msg.py %PART_NAME%\%MSG_PREFIX%_messages_hebrew.csv %GAME_PATH%\%PART_NAME%\English\%MSG_PREFIX%.MSG

if "%MSG_PREFIX%"=="7000" (
    echo Running additional command for temple2...
    python create_msg.py %PART_NAME%\%MSG_PREFIX%_messages_hebrew.csv %GAME_PATH%\temple2\English\%MSG_PREFIX%.MSG
)

echo Done!
