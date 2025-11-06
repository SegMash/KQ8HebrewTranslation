python.exe .\map_files.py .\output\1000_messages_output.txt .\output\1000_messages_output_hebrew.txt .\output\1000_mapping.txt 26
python translate_csv.py output\1000_messages.csv output\1000_mapping.txt output\1000_messages_hebrew.csv
python.exe .\create_msg.py output\1000_messages_hebrew.csv C:\Games\KQ8\daventry\English\1000.MSG