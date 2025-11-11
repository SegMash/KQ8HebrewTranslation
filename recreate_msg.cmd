python.exe .\map_files.py .\daventry\1000_messages_english.txt .\daventry\1000_messages_hebrew.txt .\daventry\1000_mapping.txt 26
python translate_csv.py daventry\1000_messages.csv daventry\1000_mapping.txt daventry\1000_messages_hebrew.csv
python.exe .\create_msg.py daventry\1000_messages_hebrew.csv C:\Games\KQ8\daventry\English\1000.MSG

python.exe .\map_files.py .\deadcity\2000_messages_english.txt .\deadcity\2000_messages_hebrew.txt .\deadcity\2000_mapping.txt 26
python translate_csv.py deadcity\2000_messages.csv deadcity\2000_mapping.txt deadcity\2000_messages_hebrew.csv
python.exe .\create_msg.py deadcity\2000_messages_hebrew.csv C:\Games\KQ8\deadcity\English\2000.MSG

python.exe .\map_files.py .\swamp\3000_messages_english.txt .\swamp\3000_messages_hebrew.txt .\swamp\3000_mapping.txt 26
python translate_csv.py swamp\3000_messages.csv swamp\3000_mapping.txt swamp\3000_messages_hebrew.csv
python.exe .\create_msg.py swamp\3000_messages_hebrew.csv C:\Games\KQ8\swamp\English\3000.MSG
