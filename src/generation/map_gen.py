import sys
import os
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.Map import Map
from generation.basic_info_gen import generate_basic_info
from generation.player_gen.player_gen import generate_player
from generation.additional_info_gen.additional_info_gen import generate_additional_info
from generation.tile_gen.tile_gen import generate_tile, generate_specific_terrain_and_sprite, get_terrain_type_sprite_range
from generation.objects_template_gen import generate_objects_template
from classes.tile.Tile import TerrainType

def generate_base_map() -> Map:
    return  Map(
        format= 28,
        basic_info= generate_basic_info(),
        players= [generate_player() for _ in range(8)],
        additional_info= generate_additional_info(),
        tiles= [generate_tile(random_terrain_sprite= False, random_terrain_type= False) for _ in range(10368)],
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

def generate_random_terrain_random_sprite_map() -> Map:
    return  Map(
        format= 28,
        basic_info= generate_basic_info(),
        players= [generate_player() for _ in range(8)],
        additional_info= generate_additional_info(),
        tiles= [generate_tile(random_terrain_sprite= True, random_terrain_type= True) for _ in range(10368)],
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

def generate_all_terrain_all_sprite_map() -> Map:
    tiles = []
    for terrain_type in list(TerrainType):
        allowed_ranges = get_terrain_type_sprite_range(terrain_type)
        for allowed_range in allowed_ranges:
            sprite_min, sprite_max = allowed_range
            for i in range(sprite_min, sprite_max + 1):
                tiles.append(generate_specific_terrain_and_sprite(terrain_type, i))

    for i in range(10368 - len(tiles)):
        tiles.append(generate_tile(random_terrain_sprite=False, random_terrain_type=False))

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