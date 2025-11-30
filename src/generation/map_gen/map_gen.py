import random
from typing import Dict

from classes.Enums.ArtifactType import ArtifactType
from classes.Enums.CastleLevel import CastleLevel
from classes.Enums.CreatureType import CreatureType
from classes.Enums.Formation import Formation
from classes.Enums.HallLevel import HallLevel
from classes.Enums.LossConditions import LossConditions
from classes.Enums.ResourceType import ResourceType
from classes.Enums.VictoryConditions import VictoryConditions
from classes.Objects.Objects import Objects
from classes.Objects.Properties.Helpers.Alignment import Alignment
from classes.Objects.Properties.Helpers.MayNotHaveSpell import MayNotHaveSpell
from classes.Objects.Properties.Helpers.MustHaveSpell import MustHaveSpell
from classes.Objects.Properties.RandomDwelling import RandomDwelling
from classes.Map import Map
from classes.Objects.Properties.Town import Town
from classes.ObjectsTemplate import ObjectsTemplate
from classes.player.Heroes import Heroes
from classes.player.MainTown import MainTown
from classes.tile.Flags import Flags

from classes.tile.Tile import TerrainType
from generation.additional_info_gen.loss_condition_gen import LossConditionParams
from generation.additional_info_gen.teams_gen import TeamsParams
from generation.additional_info_gen.victory_condition_gen import VictoryConditionParams
from generation.basic_info_gen import generate_basic_info
from generation.object_gen.json_parser import read_object_templates_from_json, read_object_from_json
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
    size: int = 72,
    player_cities: int = 8,
    players_count: int = 8,
    neutral_cities: int = 2,
    difficulty: int = 1,
    victory_condition_params: VictoryConditionParams=VictoryConditionParams(
        victory_condition=VictoryConditions.ACQUIRE_ARTIFACT, # changed from transport because it wasnt working
        artifact_type=ArtifactType.Golden_Bow,
        resource_type=ResourceType.GEMS,
        creature_type=CreatureType.Griffin,
        amount=100,
        count=150,
        x=255,
        y=255,
        z=255,
        hall_level=HallLevel.CITY,
        castle_level=CastleLevel.CASTLE,
    ),
    loss_condition_params: LossConditionParams = LossConditionParams(
        loss_condition=LossConditions.TIME_EXPIRES,
        days=6), # tu był pies pogrzebany
    teams_params: TeamsParams = None
    ) -> Map:
    """
    Generate a map using Voronoi regions to assign terrain types.
    """
    width = size
    height = size
    
    tiles = []
    generator = VoronoiMapGenerator(height=height//2, width=width//2, terrain_weights=terrain_values)
    terrain_map = generator.generate_map()

    reserved_tiles = set()

    def get_neighbours(x: int, y: int):
        directions = [(-1, -1), (0, -1), (1, -1),
                      (-1, 0),          (1, 0),
                      (-1, 1),  (0, 1),  (1, 1)]
        neighbours = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                neighbours.append((nx, ny))
        return neighbours
    
    # upscale map
    terrain_map = upscale_map(terrain_map=terrain_map)
    terrain_map = smooth_map(terrain_map=terrain_map)
    for y in range(height):
        for x in range(width):
            terrain_type = terrain_map[y][x]
            sprite_val, x_terrain_flip, y_terrain_flip = choose_sprite(terrain_map, x, y)
            if terrain_type == TerrainType.ROCK or terrain_type == TerrainType.WATER:
                reserved_tiles.add((x, y))
                for nx, ny in get_neighbours(x, y):
                    reserved_tiles.add((nx, ny))
            tiles.append(
                generate_tile(
                    terrain_type=terrain_type, terrain_sprite=sprite_val,
                    flags=Flags(terrain_x=x_terrain_flip, terrain_y=y_terrain_flip)
                )
            )

    total_cities = player_cities + neutral_cities
    total_regions = player_cities * 4 + neutral_cities  # 32 regiony (p?l)

    obj = ObjectTemplateHelper(tiles=tiles, number_of_players=players_count,
                               town_params=TownParams(player_cities, neutral_cities, 30, total_regions),
                               victory_condition_params=victory_condition_params,
                               reserved_tiles=reserved_tiles, difficulty=difficulty)
    objects_templates, objects, city_field_mapping, players, towns_generated, heroes_generated, monsters_generated = obj.initData()
    # print("\n=== WYGENEROWANE MIASTA ===")
    # for town in towns_generated:
    #     print(town.x, town.y, town.properties.name)

    # Wyswietl mapowanie miast do pol
    print("\n=== MAPOWANIE MIAST DO POL ===")
    for city_info in city_field_mapping:
        print(f"{city_info}")

    # Ensure there are always 8 player slots in the serialized map.
    # For missing players append dummy players that are inactive (won't appear on map):
    # set both can_be_human and can_be_computer to 0.
    if len(players) < 8:
        from classes.player.Player import Player as PlayerClass
        missing = 8 - len(players)
        from classes.player.StartingHero import StartingHero
        for _ in range(missing):
            p = PlayerClass.create_default()
            try:
                p.can_be_human = 0
                p.can_be_computer = 0
                p.main_town = None
                p.has_random_heroes = 0
                # ensure starting_hero exists and indicates 'none'
                try:
                    p.starting_hero = StartingHero.create_default()
                except Exception:
                    # fallback: leave existing starting_hero or set attribute if possible
                    if not hasattr(p, 'starting_hero'):
                        p.starting_hero = None
                p.num_nonspecific_placeholder_heroes = 0
                p.heroes = []
            except Exception:
                # best-effort; continue even if some attributes missing
                pass
            players.append(p)

    return Map(
        format=28,
        basic_info=generate_basic_info(map_size=size,
                        name="#Generated map",
                        description="This map has been generated",
                        difficulty=difficulty),
        players=players,
        additional_info=generate_additional_info(victory_condition_params=victory_condition_params,
                                                 loss_condition_params=loss_condition_params,
                                                 teams_params=teams_params),
        tiles=tiles,
        objects_templates=objects_templates,
        objects=objects,
        global_events=[],
        padding=[0] * 124
    ), towns_generated, heroes_generated, monsters_generated