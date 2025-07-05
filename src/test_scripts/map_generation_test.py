import os
import sys
import json
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import filedialog
import os
from classes.Map import Map

root = tk.Tk()
root.withdraw()

print("Choose a folder to save the file")
folder_path = filedialog.askdirectory(title="Select a folder to save the file")
if not folder_path:
    print("No folder selected. Exiting...")
    exit()
print("Chosen folder:", folder_path)

filename = input("Enter the file name (without extension): ").strip()
if not filename:
    print("No filename provided. Exiting...")
    exit()
print("Chosen filename:", filename)

print("Generating map representation...")
map_instance = Map.create_default()
map_representation = map_instance.to_dict()
json_str = json.dumps(map_representation, indent=2)
print("Map representation generated successfully")

file_path = os.path.join(folder_path, f"{filename}.json")

print(f"Saving map representation to: {file_path}")
try:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json_str)
    print(f"File created successfully at: {file_path}")
except Exception as e:
    print(f"Failed to create file: {e}")
