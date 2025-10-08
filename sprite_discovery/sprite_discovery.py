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
                            sprite_num = int(match.group(1))
                            if sprite_num not in sprites:
                                sprites.append(sprite_num)
    return sprites

script_dir = os.path.dirname(os.path.abspath(__file__))
known_sprites_path = os.path.join(script_dir, "known_sprites.txt")

if os.path.exists(known_sprites_path):
    known_sprites = {terrain.name: set() for terrain in TerrainType}
    with open(known_sprites_path, "r", encoding="utf-8") as f:
        for line in f:
            if ':' in line:
                terrain_name, sprite_str = line.split(':', 1)
                terrain_name = terrain_name.strip()
                sprites = [int(s) for s in sprite_str.strip().split(',') if s.strip().isdigit()]
                if terrain_name in known_sprites:
                    known_sprites[terrain_name].update(sprites)
else:
    known_sprites = {terrain.name: set() for terrain in TerrainType}

root = tk.Tk()
root.withdraw()
h3m_file_path = filedialog.askopenfilename(
    title="Select H3M file",
    filetypes=[("H3M files", "*.h3m")]
)
if not h3m_file_path:
    print("No file selected. Exiting.")
    sys.exit(0)

temp_json_path = os.path.splitext(h3m_file_path)[0] + "_temp_conversion.json"

print("Converting H3M to JSON...")
os.system(f'h3mtxt.exe "{h3m_file_path}" "{temp_json_path}"')

for terrain in TerrainType:
    sprites = extract_sprites_for_terrain(temp_json_path, terrain.value)
    known_sprites[terrain.name].update(sprites)
    print(f"{terrain.name} ({terrain.value}): {sorted(known_sprites[terrain.name])}")

with open(known_sprites_path, "w", encoding="utf-8") as f:
    for terrain_name in known_sprites:
        sprite_list = sorted(list(known_sprites[terrain_name]))
        sprite_str = ", ".join(str(s) for s in sprite_list)
        f.write(f"{terrain_name}: {sprite_str}\n")

if os.path.exists(temp_json_path):
    os.remove(temp_json_path)