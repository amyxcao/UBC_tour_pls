import os
import re
import shutil

# Regex to extract the temperature value from the filename
pattern = re.compile(r'_temp([0-9.]+)\.json$')

# Get all JSON files in the current directory
files = [f for f in os.listdir('.') if f.endswith('.json')]

for file in files:
    match = pattern.search(file)
    if match:
        temp = match.group(1)
        folder_name = f'temp{temp}'
        os.makedirs(folder_name, exist_ok=True)
        shutil.move(file, os.path.join(folder_name, file))
        print(f"Moved {file} to {folder_name}/")
    else:
        print(f"Skipped {file} (no temp match)")
