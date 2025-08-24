import os
import re
import tkinter as tk
from tkinter import filedialog
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from classes.tile.Tile import TerrainType

def extract_sprites_for_terrain(json_path: str, terrain_type_number: int) -> list[int]:
    sprites = []
    terrain_pattern = f'"terrain_type": {terrain_type_number}'
    with open(json_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if terrain_pattern in line:
                j = i + 1
                while j < len(lines) and lines[j].strip() == '':
                    j += 1
                if j < len(lines):
                    next_line = lines[j]
                    if '"terrain_sprite":' in next_line:
                        match = re.search(r'"terrain_sprite":\s*(\d+)', next_line)
                        if match:
                            sprites.append(int(match.group(1)))
    return sorted(set(sprites))

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Select JSON file",
    filetypes=[("JSON files", "*.json")]
)
if not file_path:
    print("No file selected. Exiting.")
    sys.exit(0)

terrain_type_word = input("Provide terrain type (e.g., DIRT, SAND, GRASS): ").strip().upper()
try:
    terrain_type_num = TerrainType[terrain_type_word].value
except KeyError:
    print(f"Invalid terrain type: {terrain_type_word}")
    sys.exit(1)

sprites = extract_sprites_for_terrain(file_path, terrain_type_num)
print(f"Extracted sprites for terrain type {terrain_type_word} ({terrain_type_num}): {sprites}")