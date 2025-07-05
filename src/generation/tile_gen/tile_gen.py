import sys
import os
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from classes.tile.Tile import Tile, TerrainType
from generation.tile_gen.flags_gen import generate_flags

def generate_tile() -> Tile:
    return Tile(
        terrain_type = TerrainType.WATER,
        terrain_sprite = 22,
        river_type = 0,
        river_sprite =  0,
        road_type = 0,
        road_sprite = 0,
        flags = generate_flags()
    )