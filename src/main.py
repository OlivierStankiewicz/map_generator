from generation.map_gen import MapGenerator
from classes.tile.Tile import TerrainType

import os
import json

import tkinter as tk
from tkinter import filedialog

exe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "h3mtxt.exe"))

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
map = MapGenerator.generate_all_sprites_for_given_terrain_map(terrain_type=TerrainType.DIRT)
json_map_representation = json.dumps(map.to_dict(), indent=2)
print("Map representation generated successfully")

json_file_path = os.path.join(folder_path, f"{filename}.json")
h3m_file_path = os.path.join(folder_path, f"{filename}.h3m")

print(f"Saving map representation to: {json_file_path}")
try:
    with open(json_file_path, 'w', encoding='utf-8') as f:
        f.write(json_map_representation)
    print(f"File created successfully at: {json_file_path}")
except Exception as e:
    print(f"Failed to create file: {e}")

print("Converting JSON to h3m...")
try:
    os.system(f'{exe_path} {json_file_path} {h3m_file_path}')
    print("Conversion completed successfully.")
    print(f"New file created at: {h3m_file_path}")

except Exception as e:
    print(f"Failed to convert file: {e}")
    