import sys
import os
import json
import tkinter as tk
from tkinter import filedialog
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
from generation.map_gen.map_gen import generate_voronoi_map
from classes.tile.Tile import TerrainType

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

terrain_values = {
    TerrainType.WATER: 2,
    TerrainType.GRASS: 3,
    TerrainType.SNOW: 2,
    TerrainType.SWAMP: 3,
    TerrainType.ROUGH: 1,
    TerrainType.LAVA: 1,
    TerrainType.SAND: 1,
    TerrainType.DIRT: 3,
}
map = generate_voronoi_map(terrain_values)

def filter_none_values(obj):
    """Recursively remove keys with None values from dictionaries"""
    if isinstance(obj, dict):
        return {k: filter_none_values(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [filter_none_values(item) for item in obj if item is not None]
    else:
        return obj

map_dict = filter_none_values(map.to_dict())
json_map_representation = json.dumps(map_dict, indent=2)
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
    os.system(f'h3mtxt.exe {json_file_path} {h3m_file_path}')
    print("Conversion completed successfully.")
    print(f"New file created at: {h3m_file_path}")

except Exception as e:
    print(f"Failed to convert file: {e}")