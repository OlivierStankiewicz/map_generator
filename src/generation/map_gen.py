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

class MapGenerator:
    """
    A class with methods for generating different types of maps.
    """

    @staticmethod
    def generate_base_map() -> Map:
        """
        Generate a base map with default terrain (water) and sprite.
        """
        return Map(
            format=28,
            basic_info=generate_basic_info(),
            players=[generate_player() for _ in range(8)],
            additional_info=generate_additional_info(),
            tiles=[generate_tile(random_terrain_sprite=False, random_terrain_type=False) for _ in range(10368)],
            objects_templates=[generate_objects_template()],
            objects=[],
            global_events=[],
            padding=[0] * 124
        )

    @staticmethod
    def generate_random_terrain_random_sprite_map() -> Map:
        """
        Generate a map with random terrain types and sprites.
        """
        return Map(
            format= 28,
            basic_info=generate_basic_info(),
            players=[generate_player() for _ in range(8)],
            additional_info=generate_additional_info(),
            tiles=[generate_tile(random_terrain_sprite=True, random_terrain_type=True) for _ in range(10368)],
            objects_templates=[generate_objects_template()],
            objects=[],
            global_events=[],
            padding=[0] * 124
        )

    @staticmethod
    def generate_all_terrain_all_sprite_map() -> Map:
        """
        Generate a map with all terrain types and their respective sprites.
        """
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

    @staticmethod
    def generate_map_with_terrain_constraints() -> Map:
        """
        Generate a random map for specific terrain constraints.
        
        Terrain constraints:
        - at least one of the opposite sides of a tile must border with a tile of the same terrain type (or border with the edge of the map)
        """
        width, height, depth = 72, 72, 2  # set depth = 1 for surface only
        tiles = [[[None for _ in range(width)] for _ in range(height)] for _ in range(depth)]

        for z in range(depth):  # layer (0 = surface, 1 = underground)
            y = 0
            while y < height:
                x = 0
                while x < width:
                    if depth == 1:
                        # Always Rock when no underground
                        terrain_type = TerrainType.ROCK
                        terrain_sprite = 1
                    else:
                        # Random terrain for underground-enabled maps
                        tile = generate_tile(random_terrain_type=True, random_terrain_sprite=False)
                        terrain_type = TerrainType(tile.terrain_type)
                        terrain_sprite = tile.terrain_sprite

                    # Generate a 2×2 block (respecting edges)
                    for dy in range(2):
                        for dx in range(2):
                            ny, nx = y + dy, x + dx
                            if ny < height and nx < width and tiles[z][ny][nx] is None:
                                tiles[z][ny][nx] = generate_specific_terrain_and_sprite(
                                    terrain_type=terrain_type, terrain_sprite=terrain_sprite
                                )

                    x += 2  # move in 2-tile steps horizontally
                y += 2  # move in 2-tile steps vertically

        # Flatten 3D list into 1D list for the Map class
        flat_tiles = [tile for layer in tiles for row in layer for tile in row]

        return Map(
            format=28,
            basic_info=generate_basic_info(),
            players=[generate_player() for _ in range(8)],
            additional_info=generate_additional_info(),
            tiles=flat_tiles,
            objects_templates=[generate_objects_template()],
            objects=[],
            global_events=[],
            padding=[0] * 124
        )