import os, json
from generation.map_gen import MapGenerator
from classes.tile.Tile import TerrainType


output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "generated_maps", "sand"))
h3m_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "generated_maps", "sand", "h3m"))
json_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "generated_maps", "sand", "json"))
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(h3m_folder):
    os.makedirs(h3m_folder)
if not os.path.exists(json_folder):
    os.makedirs(json_folder)

exe_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "h3mtxt.exe"))

for i in range(256):
    new_filename = f'{i}'
    print("Generating map representation...")
    map = MapGenerator.generate_given_sprite_for_given_terrain_map(terrain_type=TerrainType.SAND, terrain_sprite=i)
    json_map_representation = json.dumps(map.to_dict(), indent=2)
    print("Map representation generated successfully")  

    json_file_path = os.path.join(json_folder, f"{new_filename}.json")
    h3m_file_path = os.path.join(h3m_folder, f"{new_filename}.h3m")

    print(f"Saving json map representation...")
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