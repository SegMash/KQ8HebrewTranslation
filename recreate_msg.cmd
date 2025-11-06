python.exe .\map_files.py .\daventry\1000_messages_output.txt .\daventry\1000_messages_daventry_hebrew.txt .\daventry\1000_mapping.txt 26
python translate_csv.py daventry\1000_messages.csv daventry\1000_mapping.txt daventry\1000_messages_hebrew.csv
python.exe .\create_msg.py daventry\1000_messages_hebrew.csv C:\Games\KQ8\daventry\English\1000.MSG