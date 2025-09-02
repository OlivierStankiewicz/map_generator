import sys
import os
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from classes.tile.Tile import Tile, TerrainType
from generation.tile_gen.flags_gen import generate_flags
from random import randint, choice

def generate_tile(random_terrain_type: bool, random_terrain_sprite: bool) -> Tile:
    """
    Generate a tile with either random terrain type and sprite or default ones.
    
    :param random_terrain_type: If True, randomly selects a terrain type.
    :param random_terrain_sprite: If True, randomly selects a terrain sprite for the given terrain type.
    :return: A Tile object with the specified or random terrain type and sprite.
    """
    if random_terrain_type:
        terrain_type = choice(list(TerrainType))    
    else:
        terrain_type = TerrainType.WATER

    if random_terrain_sprite:
        sprite_ranges = get_terrain_type_sprite_range(terrain_type)
        allowed_sprites = []
        for sprite_range in sprite_ranges:
            sprite_min, sprite_max = sprite_range
            allowed_sprites.extend(range(sprite_min, sprite_max + 1))
        terrain_sprite = choice(allowed_sprites)
    else:
        terrain_sprite = 22
        
    return Tile(
        terrain_type = terrain_type,
        terrain_sprite = terrain_sprite,
        river_type = 0,
        river_sprite =  0,
        road_type = 0,
        road_sprite = 0,
        flags = generate_flags()
    )

def generate_specific_terrain_and_sprite(terrain_type: TerrainType, terrain_sprite: int) -> Tile:
    return Tile(
        terrain_type = terrain_type,
        terrain_sprite = terrain_sprite,
        river_type = 0,
        river_sprite =  0,
        road_type = 0,
        road_sprite = 0,
        flags = generate_flags()
    )

def get_terrain_type_sprite_range(terrain_type: TerrainType) -> list[tuple[int, int]]:
    if terrain_type == TerrainType.DIRT:
        return [(0, 45), (127, 173), (255, 255)]
    elif terrain_type == TerrainType.SAND:
        return [(0, 23)]
    elif terrain_type == TerrainType.GRASS:
        return [(0, 78)]
    elif terrain_type == TerrainType.SNOW:
        return [(0, 78)]
    elif terrain_type == TerrainType.SWAMP:
        return [(0, 78)]
    elif terrain_type == TerrainType.ROUGH:
        return [(0, 78)]
    elif terrain_type == TerrainType.SUBTERRANEAN:
        return [(0, 78)]
    elif terrain_type == TerrainType.LAVA:
        return [(0, 78)]
    elif terrain_type == TerrainType.WATER:
        return [(0, 32)]
    elif terrain_type == TerrainType.ROCK:
        return [(0, 47), (49, 51), (255, 255)]      #needs to be checked, generating a full rock 255 map worked, last checked 52-58, none of them worked, more exist for sure, all terrains have to be tested, max number is 255
    