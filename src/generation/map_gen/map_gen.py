from typing import Dict

from classes.Map import Map
from classes.tile.Flags import Flags
from classes.tile.Tile import TerrainType
from generation.basic_info_gen import generate_basic_info
from generation.player_gen.player_gen import generate_player
from generation.additional_info_gen.additional_info_gen import generate_additional_info
from generation.tile_gen.tile_gen import generate_tile, generate_random_tile, get_terrain_type_sprite_range
from generation.objects_template_gen import generate_objects_template
from generation.pcg_algorithms.voronoi import VoronoiMapGenerator
from generation.map_gen.utils import upscale_map, smooth_map, choose_sprite

def generate_base_map() -> Map:
    return Map(
        format= 28,
        basic_info= generate_basic_info(),
        players= [generate_player() for _ in range(8)],
        additional_info= generate_additional_info(),
        tiles= [generate_random_tile(random_terrain_sprite= False, random_terrain_type= False) for _ in range(10368)],
        objects_templates = [generate_objects_template()],
        objects= [],
        global_events= [],
        padding= [0] * 124
    )

def generate_random_terrain_random_sprite_map() -> Map:
    return Map(
        format= 28,
        basic_info= generate_basic_info(),
        players= [generate_player() for _ in range(8)],
        additional_info= generate_additional_info(),
        tiles= [generate_random_tile(random_terrain_sprite= True, random_terrain_type= True) for _ in range(10368)],
        objects_templates = [generate_objects_template()],
        objects= [],
        global_events= [],
        padding= [0] * 124
    )

def generate_all_terrain_all_sprite_map() -> Map:
    tiles = []
    for terrain_type in list(TerrainType):
        allowed_range = get_terrain_type_sprite_range(terrain_type)
        sprite_min, sprite_max = allowed_range
        for i in range(sprite_min, sprite_max + 1):
            tiles.append(generate_tile(terrain_type=terrain_type, terrain_sprite=i))

    for i in range(10368 - len(tiles)):
        tiles.append(generate_random_tile(random_terrain_sprite=False, random_terrain_type=False))

    return Map(
        format= 28,
        basic_info= generate_basic_info(),
        players= [generate_player() for _ in range(8)],
        additional_info= generate_additional_info(),
        tiles= tiles,
        objects_templates = [generate_objects_template()],
        objects= [],
        global_events= [],
        padding= [  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )

def generate_one_terrain_all_sprite_map(terrain_type: TerrainType) -> Map:
    tiles = []
        
    allowed_range = get_terrain_type_sprite_range(terrain_type)
    sprite_min, sprite_max = allowed_range
    for i in range(sprite_min, sprite_max + 1):
        tiles.append(generate_tile(terrain_type=terrain_type, terrain_sprite=i))

    for i in range(10368 - len(tiles)):
        tiles.append(generate_random_tile(random_terrain_sprite=False, random_terrain_type=False))

    return Map(
        format= 28,
        basic_info= generate_basic_info(),
        players= [generate_player() for _ in range(8)],
        additional_info= generate_additional_info(),
        tiles= tiles,
        objects_templates = [generate_objects_template()],
        objects= [],
        global_events= [],
        padding= [0] * 124
    )

def generate_sprite_comparison_map(terrain_type: TerrainType, compared_range: list[int], compared_sprite_num: int) -> Map:
    tiles = []
    sprite_min, sprite_max = compared_range
    for i in range(sprite_min, sprite_max + 1):
        tiles.append(generate_tile(terrain_type=terrain_type, terrain_sprite=i))

    for i in range(72 - len(tiles)):
        tiles.append(generate_random_tile(random_terrain_sprite=False, random_terrain_type=False))

    for i in range(len(compared_range)):
        tiles.append(generate_tile(terrain_type=terrain_type, terrain_sprite=compared_sprite_num))

    for i in range(10368 - len(tiles)):
        tiles.append(generate_random_tile(random_terrain_sprite=False, random_terrain_type=False))

    return Map(
        format= 28,
        basic_info= generate_basic_info(),
        players= [generate_player() for _ in range(8)],
        additional_info= generate_additional_info(),
        tiles= tiles,
        objects_templates = [generate_objects_template()],
        objects= [],
        global_events= [],
        padding= [0] * 124
    )

def generate_voronoi_map(
    terrain_values: Dict[TerrainType, int] = {
        TerrainType.WATER: 1,
        TerrainType.GRASS: 3,
        TerrainType.SAND: 2,
        TerrainType.DIRT: 3,
    }, 
    width: int = 72,
    height: int = 72) -> Map:
    """
    Generate a map using Voronoi regions to assign terrain types.
    """
    tiles = []
    generator = VoronoiMapGenerator(height=height//2, width=width//2, terrain_weights=terrain_values)
    terrain_map = generator.generate_map()

    # upscale map
    terrain_map = upscale_map(terrain_map=terrain_map)
    terrain_map = smooth_map(terrain_map=terrain_map)
    for y in range(height):
        for x in range(width):
            terrain_type = terrain_map[y][x]
            sprite_val, x_terrain_flip, y_terrain_flip = choose_sprite(terrain_map, x, y)
            tiles.append(
                generate_tile(
                    terrain_type=terrain_type, terrain_sprite=sprite_val,
                    flags=Flags(terrain_x=x_terrain_flip, terrain_y=y_terrain_flip)
                )
            )

    # underground
    for y in range(height):
        for x in range(width):
            tiles.append(generate_tile(terrain_type=TerrainType.ROCK, terrain_sprite=1))

    return Map(
        format=28,
        basic_info=generate_basic_info(),
        players=[generate_player() for _ in range(8)],
        additional_info=generate_additional_info(),
        tiles=tiles,
        objects_templates=[generate_objects_template()],
        objects=[],
        global_events=[],
        padding=[0] * 124
    )