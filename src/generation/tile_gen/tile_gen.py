import sys
import os
from enum import Enum
from random import choice

# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from classes.tile.Flags import Flags
from classes.tile.Tile import Tile, TerrainType
from generation.tile_gen.flags_gen import generate_flags

class SpriteType(Enum):
    SAND_OUTER_CORNER = 0
    SAND_EDGE_VERTICAL = 1
    SAND_EDGE_HORIZONTAL = 2
    SAND_INNER_CORNER = 3
    SAND_OUTER_CORNER_NEXT_TO_HALF_WATER = 4
    SAND_INNER_CORNER_NEXT_TO_HALF_WATER = 5
    SAND_CONNECTOR = 6
    CENTER = 7
    SAND = 8
    DIRT_OUTER_CORNER = 9
    DIRT_EDGE_VERTICAL = 10
    DIRT_EDGE_HORIZONTAL = 11
    DIRT_INNER_CORNER = 12
    DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER = 13
    DIRT_INNER_CORNER_NEXT_TO_HALF_WATER = 14
    DIRT_CONNECTOR = 15
    DIRT = 16
    MIXED_CONNECTOR = 17
    MIXED_OUTER_CORNER_VERTICAL_SAND = 18   # SAND CONNECTION IS VERTICAL
    MIXED_OUTER_CORNER_HORIZONTAL_SAND = 19 # SAND CONNECTION IS HORIZONTAL
    MIXED_EDGE_HORIZONTAL = 20              # NATIVE TERRAIN EDGE IS HORIZONTAL
    MIXED_EDGE_VERTICAL = 21                # NATIVE TERRAIN EDGE IS VERTICAL
    MIXED_OUTER_CORNER_VERTICAL_DIRT = 22   # DIRT CONNECTION IS VERTICAL
    MIXED_OUTER_CORNER_HORIZONTAL_DIRT = 23 # DIRT CONNECTION IS HORIZONTAL
    MIXED_OUTER_CORNER_NEXT_TO_HALF_WATER = 24
    MIXED_INNER_CORNER_NEXT_TO_HALF_WATER = 25
    MIXED_CONNECTOR_BETWEEN_HALF_WATERS = 26
    MIXED_OUTER_CORNER_DIAGONAL_SAND = 27

def generate_random_tile(random_terrain_type: bool, random_terrain_sprite: bool) -> Tile:
    if random_terrain_type:
        terrain_type = choice(list(TerrainType))    
    else:
        terrain_type = TerrainType.WATER

    if random_terrain_sprite:
        sprite_range = get_terrain_type_sprite_range(terrain_type) 
        sprite_min, sprite_max = sprite_range
        allowed_sprites = range(sprite_min, sprite_max + 1)
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

def generate_tile(terrain_type: TerrainType = TerrainType.WATER,
                  terrain_sprite: int = 0,
                  river_type: int = 0,
                  river_sprite: int = 0,
                  road_type: int = 0,
                  road_sprite: int = 0,
                  flags: Flags = generate_flags()) -> Tile:
    return Tile(
        terrain_type = terrain_type,
        terrain_sprite = terrain_sprite,
        river_type = river_type,
        river_sprite = river_sprite,
        road_type = road_type,
        road_sprite = road_sprite,
        flags = flags
    )

def get_terrain_type_sprite_range(terrain_type: TerrainType) -> tuple[int, int]:
    if terrain_type == TerrainType.DIRT:
        return (0, 45)
    elif terrain_type == TerrainType.SAND:
        return (0, 23)
    elif terrain_type == TerrainType.GRASS:
        return (0, 78)
    elif terrain_type == TerrainType.SNOW:
        return (0, 78)
    elif terrain_type == TerrainType.SWAMP:
        return (0, 78)
    elif terrain_type == TerrainType.ROUGH:
        return (0, 78)
    elif terrain_type == TerrainType.SUBTERRANEAN:
        return (0, 78)
    elif terrain_type == TerrainType.LAVA:
        return (0, 78)
    elif terrain_type == TerrainType.WATER:
        return (0, 32)
    elif terrain_type == TerrainType.ROCK:
        return (0, 47)

def get_terrain_type_sprite_type_range(terrain_type: TerrainType, sprite_type: SpriteType) -> dict[str, tuple]:
    sprite_groups = {
        TerrainType.DIRT: {
            SpriteType.SAND_OUTER_CORNER: { "standard": (0, 3), "special": () },
            SpriteType.SAND_EDGE_VERTICAL: { "standard": (4, 7), "special": () },
            SpriteType.SAND_EDGE_HORIZONTAL: { "standard": (8, 11), "special": () },
            SpriteType.SAND_INNER_CORNER: { "standard": (12, 15), "special": () },
            SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER: { "standard": (16, 17), "special": () },
            SpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER: { "standard": (18, 19), "special": () },
            SpriteType.SAND_CONNECTOR: { "standard": (20, 20), "special": () },
            SpriteType.CENTER: { "standard": (21, 28), "special": (29, 44) },
            SpriteType.SAND: { "standard": (45, 45), "special": () }
        },

        TerrainType.SAND: {
            SpriteType.CENTER: { "standard": (0, 7), "special": (8, 23) }
        },

        "dirt_based_terrain_without_dirt": {
            SpriteType.SAND_OUTER_CORNER: { "standard": (20, 23), "special": () },
            SpriteType.SAND_EDGE_VERTICAL: { "standard": (24, 27), "special": () },
            SpriteType.SAND_EDGE_HORIZONTAL: { "standard": (28, 31), "special": () },
            SpriteType.SAND_INNER_CORNER: { "standard": (32, 35), "special": () },
            SpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER: { "standard": (36, 37), "special": () },
            SpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER: { "standard": (38, 39), "special": () },
            SpriteType.SAND_CONNECTOR: { "standard": (42, 42), "special": () },
            SpriteType.CENTER: { "standard": (49, 56), "special": (57, 72) },
            SpriteType.SAND: { "standard": (74, 74), "special": () },
            SpriteType.DIRT_OUTER_CORNER: { "standard": (0, 3), "special": () },
            SpriteType.DIRT_EDGE_VERTICAL: { "standard": (4, 7), "special": () },
            SpriteType.DIRT_EDGE_HORIZONTAL: { "standard": (8, 11), "special": () },
            SpriteType.DIRT_INNER_CORNER: { "standard": (12, 15), "special": () } ,
            SpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER: { "standard": (16, 17), "special": () },
            SpriteType.DIRT_INNER_CORNER_NEXT_TO_HALF_WATER: { "standard": (18, 19), "special": () },
            SpriteType.DIRT_CONNECTOR: { "standard": (40, 40), "special": () },
            SpriteType.DIRT: { "standard": (73, 73), "special": () },
            SpriteType.MIXED_CONNECTOR: { "standard": (41, 41), "special": () },
            SpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND: { "standard": (47, 47), "special": () },
            SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND: { "standard": (48, 48), "special": () },
            SpriteType.MIXED_EDGE_VERTICAL: { "standard": (45, 45), "special": () },
            SpriteType.MIXED_EDGE_HORIZONTAL: { "standard": (46, 46), "special": () },
            SpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT: { "standard": (43, 43), "special": () },
            SpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT: { "standard": (44, 44), "special": () },
            SpriteType.MIXED_INNER_CORNER_NEXT_TO_HALF_WATER: { "standard": (75, 75), "special": () },
            SpriteType.MIXED_OUTER_CORNER_NEXT_TO_HALF_WATER: { "standard": (76, 76), "special": () },
            SpriteType.MIXED_CONNECTOR_BETWEEN_HALF_WATERS: { "standard": (77, 77), "special": () },
            SpriteType.MIXED_OUTER_CORNER_DIAGONAL_SAND: { "standard": (78, 78), "special": () }
        }
    }

    dirt_based_group_without_dirt = {TerrainType.GRASS, TerrainType.SNOW, TerrainType.SWAMP, TerrainType.ROUGH, TerrainType.SUBTERRANEAN, TerrainType.LAVA}
    if terrain_type in dirt_based_group_without_dirt:
        terrain_type = "dirt_based_terrain_without_dirt"
    
    return sprite_groups[terrain_type][sprite_type]