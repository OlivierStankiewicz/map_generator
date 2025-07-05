import sys
import os
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from classes.tile.Tile import Tile, TerrainType
from generation.tile_gen.flags_gen import generate_flags
from random import randint, choice

def generate_tile(random_terrain_type: bool, random_terrain_sprite: bool) -> Tile:
    terrain_type = choice(list(TerrainType)) if random_terrain_type else TerrainType.WATER
    terrain_sprite = randint(0, 32) if random_terrain_sprite else 22    # 0-32 works for water, not for all other terrain types, 22 works for all terrain types
    return Tile(
        terrain_type = terrain_type,
        terrain_sprite = terrain_sprite,
        river_type = 0,
        river_sprite =  0,
        road_type = 0,
        road_sprite = 0,
        flags = generate_flags()
    )