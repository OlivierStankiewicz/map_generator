import random
from typing import Dict

from classes.Map import Map
from classes.tile.Tile import TerrainType
from generation.basic_info_gen import generate_basic_info
from generation.player_gen.player_gen import generate_player
from generation.additional_info_gen.additional_info_gen import generate_additional_info
from generation.tile_gen.tile_gen import generate_tile, generate_specific_terrain_and_sprite, get_terrain_type_sprite_range
from generation.objects_template_gen import generate_objects_template
from generation.pcg_algorithms.perlin import perlin
from generation.pcg_algorithms.voronoi import voronoi
from generation.map_gen.utils import upscale_map, smooth_map

def generate_base_map() -> Map:
    return Map(
        format= 28,
        basic_info= generate_basic_info(),
        players= [generate_player() for _ in range(8)],
        additional_info= generate_additional_info(),
        tiles= [generate_tile(random_terrain_sprite= False, random_terrain_type= False) for _ in range(10368)],
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
        tiles= [generate_tile(random_terrain_sprite= True, random_terrain_type= True) for _ in range(10368)],
        objects_templates = [generate_objects_template()],
        objects= [],
        global_events= [],
        padding= [0] * 124
    )

def generate_all_terrain_all_sprite_map() -> Map:
    tiles = []
    for terrain_type in TerrainType:
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
        padding= [0] * 124
    )

def generate_perlin_noise_map(width=72, height=72, scale=10.0, octaves=2, persistence=0.5, lacunarity=2.0, seed=None) -> Map:
    """
    Generate a Map using Perlin noise to assign terrain types.
    """
    if seed is not None:
        random.seed(seed)

    tiles = []
    terrain_types = list(TerrainType)
    num_types = len(terrain_types)

    small_width, small_height = width // 2, height // 2
    terrain_map = [[None for _ in range(small_width)] for _ in range(small_height)]

    for y in range(small_height):
        for x in range(small_width):
            amplitude = 1.0
            frequency = 1.0
            value = 0.0
            max_amp = 0.0

            for _ in range(octaves):
                sample_x = (x / scale) * frequency
                sample_y = (y / scale) * frequency
                n = perlin(sample_x, sample_y)

                value += n * amplitude
                max_amp += amplitude
                amplitude *= persistence
                frequency *= lacunarity

            normalized = (value / max_amp + 1) / 2  # map [-1,1] -> [0,1]
            terrain_index = round(normalized * (num_types - 1))
            terrain_map[y][x] = terrain_types[terrain_index]

    # upscale map
    upscaled_terrain_map = upscale_map(map=terrain_map)
    for y in range(height):
        for x in range(width):
            terrain_type = upscaled_terrain_map[y][x]
            tiles.append(generate_specific_terrain_and_sprite(terrain_type, 1))

    # underground
    for y in range(height):
        for x in range(width):
            tiles.append(generate_specific_terrain_and_sprite(TerrainType.ROCK, 1))

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
    terrain_map = voronoi(terrain_values=terrain_values, height=height//2, width=width//2)

    # upscale map
    upscaled_terrain_map = upscale_map(map=terrain_map)
    upscaled_terrain_map = smooth_map(terrain_map=upscaled_terrain_map)
    for y in range(height):
        for x in range(width):
            terrain_type = upscaled_terrain_map[y][x]
            tiles.append(generate_specific_terrain_and_sprite(terrain_type, 1))

    # underground
    for y in range(height):
        for x in range(width):
            tiles.append(generate_specific_terrain_and_sprite(TerrainType.ROCK, 1))

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

