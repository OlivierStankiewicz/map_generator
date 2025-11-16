import random
from typing import Dict

from classes.Objects.Objects import Objects
from classes.Objects.Properties.Helpers.Alignment import Alignment
from classes.Objects.Properties.RandomDwelling import RandomDwelling
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

from generation.object_gen.object_template_helper import ObjectTemplateHelper, TownParams
from generation.object_gen.objects_template_gen import generate_objects_template_and_objects


def generate_base_map() -> Map:
    return Map(
        format= 28,
        basic_info= generate_basic_info(),
        players= [generate_player() for _ in range(8)],
        additional_info= generate_additional_info(),
        tiles= [generate_tile(random_terrain_sprite= False, random_terrain_type= False) for _ in range(10368)],
        objects_templates = [generate_objects_template_and_objects()],
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
        tiles= [generate_tile(random_terrain_sprite= True, random_terrain_type= True) for _ in range(10368)],
        objects_templates = [generate_objects_template_and_objects()],
        objects= [],
        global_events= [],
        padding= [0] * 124
    )

def generate_all_terrain_all_sprite_map() -> Map:
    tiles = []
    for terrain_type in TerrainType:
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
        objects_templates = [generate_objects_template_and_objects()],
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

    for i in tiles:
        if i.terrain_type == TerrainType.DIRT:
            print(f"{i.terrain_type}")

    player_cities = 4
    neutral_cities = 2
    total_cities = player_cities + neutral_cities
    total_regions = total_cities * 4  # 32 regiony (p?l)

    obj = ObjectTemplateHelper(tiles=tiles, townParams=TownParams(4, 2, 30, total_regions), numberOfPlayers=8)
    objects_templates, objects, city_field_mapping = obj.initData()

    # Wyswietl mapowanie miast do pol
    print("\n=== MAPOWANIE MIAST DO POL ===")
    for city_info in city_field_mapping:
        print(f"{city_info}")

    return Map(
        format=28,
        basic_info=generate_basic_info(),
        players=[generate_player() for _ in range(8)],
        additional_info=generate_additional_info(),
        tiles=tiles,
        objects_templates=objects_templates,
        objects=objects,
        global_events=[],
        padding=[0] * 124
    )