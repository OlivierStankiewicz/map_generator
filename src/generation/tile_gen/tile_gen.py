from enum import Enum
from random import choice

from classes.tile.Flags import Flags
from classes.tile.Tile import Tile, TerrainType, RiverType, RoadType
from generation.tile_gen.flags_gen import generate_flags

class TerrainSpriteType(Enum):
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
    
    # rock
    UPPER_LEFT_OUTER_CORNER = 28
    UPPER_RIGHT_OUTER_CORNER = 29
    LOWER_LEFT_OUTER_CORNER = 30
    LOWER_RIGHT_OUTER_CORNER = 31
    LEFT_VERTICAL = 32
    RIGHT_VERTICAL = 33
    UPPER_HORIZONTAL = 34
    LOWER_HORIZONTAL = 35
    UPPER_LEFT_INNER_CORNER = 36
    UPPER_RIGHT_INNER_CORNER = 37
    LOWER_LEFT_INNER_CORNER = 38
    LOWER_RIGHT_INNER_CORNER = 39
    UPPER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER = 40
    UPPER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER = 41
    LOWER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER = 42
    LOWER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER = 43
    UPPER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER = 44
    UPPER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER = 45
    LOWER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER = 46
    LOWER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER = 47    

class RoadSpriteType(Enum):
    CORNER = 0
    FLATTENED_CORNER = 1
    ONE_WAY_CROSSING_VERTICAL = 2
    ONE_WAY_CROSSING_HORIZONTAL = 3
    VERTICAL = 4
    HORIZONTAL = 5
    VERTICAL_END = 6
    HORIZONTAL_END = 7
    TWO_WAY_CROSSING = 8
    
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
        river_type = RiverType.NONE,
        river_sprite =  0,
        road_type = RoadType.NONE,
        road_sprite = 0,
        flags = generate_flags()
    )

def generate_tile(terrain_type: TerrainType = TerrainType.WATER,
                  terrain_sprite: int = 0,
                  river_type: RiverType = RiverType.NONE,
                  river_sprite: int = 0,
                  road_type: RoadType = RoadType.NONE,
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

def get_terrain_type_sprite_type_range(terrain_type: TerrainType, sprite_type: TerrainSpriteType) -> dict[str, tuple]:
    sprite_groups = {
        TerrainType.SAND: {
            TerrainSpriteType.CENTER: { "standard": (0, 7), "special": (8, 23) }
        },
        
        TerrainType.WATER: {
            TerrainSpriteType.SAND_OUTER_CORNER: { "standard": (0, 3), "special": () },
            TerrainSpriteType.SAND_EDGE_VERTICAL: { "standard": (4, 7), "special": () },
            TerrainSpriteType.SAND_EDGE_HORIZONTAL: { "standard": (8, 11), "special": () },
            TerrainSpriteType.SAND_INNER_CORNER: { "standard": (12, 15), "special": () },
            TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER: { "standard": (16, 17), "special": () },
            TerrainSpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER: { "standard": (18, 19), "special": () },
            TerrainSpriteType.CENTER: { "standard": (21, 32), "special": () },
        },
        
        TerrainType.ROCK: {
            TerrainSpriteType.CENTER: { "standard": (0, 7), "special": () },
            TerrainSpriteType.UPPER_LEFT_OUTER_CORNER: { "standard": (8, 9), "special": () },
            TerrainSpriteType.UPPER_RIGHT_OUTER_CORNER: { "standard": (10, 11), "special": () },
            TerrainSpriteType.LOWER_LEFT_OUTER_CORNER: { "standard": (12, 13), "special": () },
            TerrainSpriteType.LOWER_RIGHT_OUTER_CORNER: { "standard": (14, 15), "special": () },
            TerrainSpriteType.LEFT_VERTICAL: { "standard": (16, 17), "special": () },
            TerrainSpriteType.RIGHT_VERTICAL: { "standard": (18, 19), "special": () },
            TerrainSpriteType.UPPER_HORIZONTAL: { "standard": (20, 21), "special": () },
            TerrainSpriteType.LOWER_HORIZONTAL: { "standard": (22, 23), "special": () },
            TerrainSpriteType.UPPER_LEFT_INNER_CORNER: { "standard": (24, 25), "special": () },
            TerrainSpriteType.UPPER_RIGHT_INNER_CORNER: { "standard": (26, 27), "special": () },
            TerrainSpriteType.LOWER_LEFT_INNER_CORNER: { "standard": (28, 29), "special": () },
            TerrainSpriteType.LOWER_RIGHT_INNER_CORNER: { "standard": (30, 31), "special": () },
            TerrainSpriteType.UPPER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER: { "standard": (32, 33), "special": () },
            TerrainSpriteType.UPPER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER: { "standard": (34, 35), "special": () },
            TerrainSpriteType.LOWER_LEFT_OUTER_CORNER_NEXT_TO_HALF_WATER: { "standard": (36, 37), "special": () },
            TerrainSpriteType.LOWER_RIGHT_OUTER_CORNER_NEXT_TO_HALF_WATER: { "standard": (38, 39), "special": () },
            TerrainSpriteType.UPPER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER: { "standard": (40, 41), "special": () },
            TerrainSpriteType.UPPER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER: { "standard": (42, 43), "special": () },
            TerrainSpriteType.LOWER_LEFT_INNER_CORNER_NEXT_TO_HALF_WATER: { "standard": (44, 45), "special": () },
            TerrainSpriteType.LOWER_RIGHT_INNER_CORNER_NEXT_TO_HALF_WATER: { "standard": (46, 47), "special": () }
        },
        
        TerrainType.DIRT: {
            TerrainSpriteType.SAND_OUTER_CORNER: { "standard": (0, 3), "special": () },
            TerrainSpriteType.SAND_EDGE_VERTICAL: { "standard": (4, 7), "special": () },
            TerrainSpriteType.SAND_EDGE_HORIZONTAL: { "standard": (8, 11), "special": () },
            TerrainSpriteType.SAND_INNER_CORNER: { "standard": (12, 15), "special": () },
            TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER: { "standard": (16, 17), "special": () },
            TerrainSpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER: { "standard": (18, 19), "special": () },
            TerrainSpriteType.SAND_CONNECTOR: { "standard": (20, 20), "special": () },
            TerrainSpriteType.CENTER: { "standard": (21, 28), "special": (29, 44) },
            TerrainSpriteType.SAND: { "standard": (45, 45), "special": () }
        },

        "dirt_based_terrain_without_dirt": {
            TerrainSpriteType.SAND_OUTER_CORNER: { "standard": (20, 23), "special": () },
            TerrainSpriteType.SAND_EDGE_VERTICAL: { "standard": (24, 27), "special": () },
            TerrainSpriteType.SAND_EDGE_HORIZONTAL: { "standard": (28, 31), "special": () },
            TerrainSpriteType.SAND_INNER_CORNER: { "standard": (32, 35), "special": () },
            TerrainSpriteType.SAND_OUTER_CORNER_NEXT_TO_HALF_WATER: { "standard": (36, 37), "special": () },
            TerrainSpriteType.SAND_INNER_CORNER_NEXT_TO_HALF_WATER: { "standard": (38, 39), "special": () },
            TerrainSpriteType.SAND_CONNECTOR: { "standard": (42, 42), "special": () },
            TerrainSpriteType.CENTER: { "standard": (49, 56), "special": (57, 72) },
            TerrainSpriteType.SAND: { "standard": (74, 74), "special": () },
            TerrainSpriteType.DIRT_OUTER_CORNER: { "standard": (0, 3), "special": () },
            TerrainSpriteType.DIRT_EDGE_VERTICAL: { "standard": (4, 7), "special": () },
            TerrainSpriteType.DIRT_EDGE_HORIZONTAL: { "standard": (8, 11), "special": () },
            TerrainSpriteType.DIRT_INNER_CORNER: { "standard": (12, 15), "special": () } ,
            TerrainSpriteType.DIRT_OUTER_CORNER_NEXT_TO_HALF_WATER: { "standard": (16, 17), "special": () },
            TerrainSpriteType.DIRT_INNER_CORNER_NEXT_TO_HALF_WATER: { "standard": (18, 19), "special": () },
            TerrainSpriteType.DIRT_CONNECTOR: { "standard": (40, 40), "special": () },
            TerrainSpriteType.DIRT: { "standard": (73, 73), "special": () },
            TerrainSpriteType.MIXED_CONNECTOR: { "standard": (41, 41), "special": () },
            TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_SAND: { "standard": (47, 47), "special": () },
            TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_SAND: { "standard": (48, 48), "special": () },
            TerrainSpriteType.MIXED_EDGE_VERTICAL: { "standard": (45, 45), "special": () },
            TerrainSpriteType.MIXED_EDGE_HORIZONTAL: { "standard": (46, 46), "special": () },
            TerrainSpriteType.MIXED_OUTER_CORNER_VERTICAL_DIRT: { "standard": (43, 43), "special": () },
            TerrainSpriteType.MIXED_OUTER_CORNER_HORIZONTAL_DIRT: { "standard": (44, 44), "special": () },
            TerrainSpriteType.MIXED_INNER_CORNER_NEXT_TO_HALF_WATER: { "standard": (75, 75), "special": () },
            TerrainSpriteType.MIXED_OUTER_CORNER_NEXT_TO_HALF_WATER: { "standard": (76, 76), "special": () },
            TerrainSpriteType.MIXED_CONNECTOR_BETWEEN_HALF_WATERS: { "standard": (77, 77), "special": () },
            TerrainSpriteType.MIXED_OUTER_CORNER_DIAGONAL_SAND: { "standard": (78, 78), "special": () }
        }
    }

    dirt_based_group_without_dirt = {TerrainType.GRASS, TerrainType.SNOW, TerrainType.SWAMP, TerrainType.ROUGH, TerrainType.SUBTERRANEAN, TerrainType.LAVA}
    if terrain_type in dirt_based_group_without_dirt:
        terrain_type = "dirt_based_terrain_without_dirt"
    
    return sprite_groups[terrain_type][sprite_type]

def get_road_type_sprite_range() -> tuple[int, int]:
    return (0, 16)

def get_road_type_sprite_type_range() -> dict[RoadType, tuple]:
    return {
        TerrainSpriteType.CORNER: (0, 1),
        TerrainSpriteType.FLATTENED_CORNER: (2, 5),
        TerrainSpriteType.ONE_WAY_CROSSING_VERTICAL: (6, 7),
        TerrainSpriteType.ONE_WAY_CROSSING_HORIZONTAL: (8, 9),
        TerrainSpriteType.VERTICAL: (10, 11),
        TerrainSpriteType.HORIZONTAL: (12, 13),
        TerrainSpriteType.VERTICAL_END: (14, 14),
        TerrainSpriteType.HORIZONTAL_END: (15, 15),
        TerrainSpriteType.TWO_WAY_CROSSING: (16, 16),
    }