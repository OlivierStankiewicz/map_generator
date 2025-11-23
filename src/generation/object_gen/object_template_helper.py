import os
import sys
from collections import deque
from copy import copy
from dataclasses import dataclass
from random import randint, choices, sample
from math import sqrt

from classes.Enums.ArtifactType import converterTypeToNum as ar_converterTypeToNum
from classes.Enums.CreatureType import converterTypeToNum as cr_converterTypeToNum
from classes.Enums.Disposition import Disposition
from classes.Enums.VictoryConditions import VictoryConditions
from classes.Objects.Properties.Artifact import Artifact
from classes.Objects.Properties.Helpers.Artifacts import Artifacts
from classes.Objects.Properties.Helpers.Creatures import Creatures
from classes.Objects.Properties.Helpers.Guardians import Guardians
from classes.Objects.Properties.Helpers.PrimarySkills import PrimarySkills
from classes.Objects.Properties.Helpers.SecondarySkills import SecondarySkills
from classes.Objects.Properties.Helpers.Spells import Spells
from classes.Enums.Heroes import Hero as HeroEnum
from classes.Objects.Properties.Hero import Hero
from classes.Objects.Properties.Monster import Monster
from classes.Objects.Properties.RandomDwellingPresetAlignment import RandomDwellingPresetAlignment
from classes.Objects.Properties.Scholar import Scholar
from classes.Objects.Properties.SeersHut import SeersHut
from classes.Objects.Properties.Shrine import Shrine
from classes.Objects.Properties.TrivialOwnedObject import TrivialOwnedObject
from classes.Objects.Properties.WitchHut import WitchHut
from classes.player.Heroes import Heroes
from classes.player.MainTown import MainTown
from classes.player.StartingHero import StartingHero
from generation.additional_info_gen.loss_condition_gen import LossConditionParams
from generation.additional_info_gen.victory_condition_gen import VictoryConditionParams
from generation.player_gen.player_gen import generate_player

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from classes.Objects.Objects import Objects

from classes.Enums.Formation import Formation
from classes.Enums.TownType import TownType
from classes.Objects.Properties.Helpers.MayNotHaveSpell import MayNotHaveSpell
from classes.Objects.Properties.Helpers.MustHaveSpell import MustHaveSpell
from classes.Objects.Properties.Town import Town
from classes.Objects.Properties.RandomDwelling import RandomDwelling
from classes.Objects.Properties.Helpers.Alignment import Alignment
from classes.ObjectsTemplate import ObjectsTemplate
from classes.tile.Tile import Tile, TerrainType
from generation.object_gen.json_parser import read_object_templates_from_json, read_object_from_json
from generation.object_gen.voronoi_city_placement import generate_city_positions, generate_city_positions_with_fields, get_region_tiles


@dataclass
class TownParams:
    """Parameters for Town."""
    player_cities: int
    neutral_cities: int
    min_distance: int
    total_regions: int


class ObjectTemplateHelper:
    def __init__(self, tiles: list[Tile], townParams: TownParams, numberOfPlayers: int = 8,
                 victory_condition_params: VictoryConditionParams = None, reserved_tiles: set[tuple[int, int]] = set()):
        self.id = 1
        self.absod_id = 0
        self.tiles: list[Tile] = tiles
        self.objectTemplates: list[ObjectsTemplate] = []
        self.objects: list[Objects] = []
        self.players = [generate_player() for _ in range(8)]

        self.towns = read_object_templates_from_json("towns")
        self.dwellings_random = read_object_templates_from_json("random_dwellings")  # 0-8 RANDOM_DWELLING_PRESET_ALIGNMENT; 9 RANDOM_DWELLING; 10 - 16 RANDOM_DWELLING_PRESET_LEVEL
        self.dwellings = read_object_templates_from_json("dwellings")
        self.heroes = read_object_templates_from_json("heroes")
        self.heroes_specification = read_object_from_json("heroes_specification")
        self.mines = read_object_templates_from_json("mines")
        self.reserved_tiles = reserved_tiles

        self.map_format = int(sqrt(len(self.tiles) / 2))

        self.result = None

        # Tablica dwuwymiarowa do sledzenia zajetych miejsc na mapie
        # True = miejsce zajete/nieprzejezdne, False = miejsce wolne/przejezdne
        self.occupied_tiles = [[False for _ in range(self.map_format)] for _ in range(self.map_format)]
        self.occupied_tiles_excluding_landscape = [[False for _ in range(self.map_format)] for _ in range(self.map_format)]
        self.city_field_mapping = []  # Lista do przechowywania mapowania miast do p�l
        self.final_city_positions: list[tuple[int, int, int]] = [] # TownType.value, pos_x, pos_y

        ### params ###
        self.townParams = townParams
        self.numberOfPlayers = numberOfPlayers
        self.occ = []
        self.victory_condition_params = victory_condition_params


    def initData(self):
        # Generate positions and all regions
        self.result = generate_city_positions_with_fields(
            self.map_format,
            self.townParams.player_cities,
            self.townParams.neutral_cities,
            self.townParams.min_distance,
            self.townParams.total_regions,
            self.reserved_tiles
        )

        # test = ObjectsTemplate.create_default()
        # test.passability = [255, 255, 255, 255, 255, 254]
        # test.actionability = [0, 0, 0, 0, 0, 0]
        # self.mark_object_tiles_as_occupied(test, 0, 0, 3)

        self.create_default_object_template()
        # warstwa 2 zamki i bohaterowie
        self.generate_cities_precise_positioning()
        self.generate_heroes_positioning()
        # warstwa 2.5 win/lose condition
        self.generate_win_lose_condition()
        # warstwa 3 budynki do rekrutacji
        self.generate_dwelling_precise_positioning()
        # warstwa 4 budowle specjalne
        self.generate_special_building()

        # self.occ.sort()
        # for i in self.occ:
        #     print(i)

        return self.objectTemplates, self.objects, self.city_field_mapping, self.players

    def create_default_object_template(self):
        self.objectTemplates.append(ObjectsTemplate.create_default())
        self.objectTemplates.append(
            ObjectsTemplate("AVLholg0.def", [255, 255, 255, 255, 255, 255], [0, 0, 0, 0, 0, 0], [4, 0], [4, 0], 124, 0,
                            0, 1))

    def mark_object_tiles_as_occupied(self, template: ObjectsTemplate, x: int, y: int, offset: int = 0):
        """
        Oznacza kafelki obiektu jako zajete na podstawie passability i actionability.

        Args:
            template: Template obiektu zawierajacy passability i actionability
            x, y: Pozycja obiektu na mapie (lewy gorny rog)
            offset: obwodka na okolo obiektu, w ktorej nie chcemy aby stawiany byl inny obiekty (poza krajobrazem)
        """
        if not template.passability:
            return

        rows = 6
        cols = 8

        for row in range(rows):
            for col in range(cols):
                tile_x = x - 7 + col
                tile_y = y - 5 + row

                passable = bool(not (template.passability[row] >> (7 - col)) & 1)
                actionable = bool((template.actionability[row] >> (7 - col)) & 1)

                # Oznacz kafelek jako zajety jesli jest nieprzejezdny lub akcjonowalny
                if passable or actionable:
                    self.occupied_tiles_excluding_landscape[tile_y][tile_x] = True
                    # oznaczaj obszar z offsetem w macierzy glównej
                    for dy in range(-offset, offset + 1):
                        for dx in range(-offset, offset + 1):
                            nx = tile_x + dx
                            ny = tile_y + dy
                            if 0 <= nx < self.map_format and 0 <= ny < self.map_format:
                                self.occupied_tiles[ny][nx] = True


    def get_occupied_tiles_count(self) -> int:
        """Zwraca liczbe zajetych kafelkow na mapie"""
        count = 0
        for row in self.occupied_tiles:
            for tile in row:
                if tile:
                    count += 1
        return count

    def print_occupation_stats(self):
        """Wyswietla statystyki zajetosci mapy"""
        total_tiles = self.map_format * self.map_format
        occupied_count = self.get_occupied_tiles_count()
        free_count = total_tiles - occupied_count
        occupation_percentage = (occupied_count / total_tiles) * 100

        print(f"Statystyki zajetosci mapy {self.map_format}x{self.map_format}:")
        print(f"  Zajete kafelki: {occupied_count}")
        print(f"  Wolne kafelki: {free_count}")
        print(f"  Procent zajetosci: {occupation_percentage:.2f}%")

    def validate_placement(self, template: ObjectsTemplate, x: int, y: int) -> bool:
        # Sprawdz czy pozycja jest w granicach mapy (główny punkt)
        if x < 0 or x >= self.map_format or y < 0 or y >= self.map_format:
            return False

        if not template.passability:
            return False

        rows = 6
        cols = 8

        for row in range(rows):
            for col in range(cols):
                tile_x = x - 7 + col
                tile_y = y - 5 + row

                passable = bool(not (template.passability[row] >> (7 - col)) & 1)
                # print((tile_x, tile_y), passable)
                actionable = bool((template.actionability[row] >> (7 - col)) & 1)
                # print((tile_x, tile_y), actionable)

                # Jeśli kafelek, który obiekt by zajmował, leży poza mapą -> invalid
                if not (0 <= tile_x < self.map_format - 2 and 2 <= tile_y < self.map_format - 2):
                    if passable or actionable:
                        # obiekt wychodzi poza mapę
                        return False
                    continue

                if passable or actionable:
                    if self.tiles[tile_y * self.map_format + tile_x] != TerrainType.WATER and self.tiles[tile_y * self.map_format + tile_x] != TerrainType.ROCK and self.occupied_tiles[tile_y][tile_x]:
                        # print(f"Pozycja ({x}, {y}) - kolizja na kafelku ({tile_x}, {tile_y})")
                        return False

        return True

    def validate_placement_for_landscape(self, template: ObjectsTemplate, x: int, y: int) -> bool:
        # Sprawdz czy pozycja jest w granicach mapy (główny punkt)
        if x < 0 or x >= self.map_format or y < 0 or y >= self.map_format:
            return False

        if not template.passability:
            return False

        rows = 6
        cols = 8

        for row in range(rows):
            for col in range(cols):
                tile_x = x - 7 + col
                tile_y = y - 5 + row

                passable = bool(not (template.passability[row] >> (7 - col)) & 1)
                # print((tile_x, tile_y), passable)
                actionable = bool((template.actionability[row] >> (7 - col)) & 1)
                # print((tile_x, tile_y), actionable)

                # Jeśli kafelek, który obiekt by zajmował, leży poza mapą -> invalid
                if not (0 <= tile_x < self.map_format and 0 <= tile_y < self.map_format):
                    if passable or actionable:
                        # obiekt wychodzi poza mapę
                        return False
                    continue

                if passable or actionable:
                    if self.occupied_tiles_excluding_landscape[tile_y][tile_x]:
                        # print(f"Pozycja ({x}, {y}) - kolizja na kafelku ({tile_x}, {tile_y})")
                        return False

        return True

    def find_alternative_position(self, template: ObjectsTemplate, preferred_x: int, preferred_y: int,
                                  max_offset: int = 3, validation_function = None) -> tuple:
        """
        Znajduje alternatywna pozycje dla obiektu w poblizu preferowanej pozycji.
        Zwraca (x, y) jesli znajdzie wolne miejsce, lub (None, None) jesli nie.
        """
        # Default validation function
        if validation_function is None:
            validation_function = self.validate_placement

        # Najpierw sprobuj preferowana pozycje
        if validation_function(template, preferred_x, preferred_y):
            # self.occ.append((preferred_x, preferred_y))
            return preferred_x, preferred_y

        # Sprobuj pozycje w coraz wiekszych okreslach wokol preferowanej pozycji
        for offset in range(1, max_offset + 1):
            for dx in range(-offset, offset + 1):
                for dy in range(-offset, offset + 1):
                    if abs(dx) == offset or abs(dy) == offset:  # Tylko krawedzie prostokata
                        new_x = preferred_x + dx
                        new_y = preferred_y + dy

                        if validation_function(template, new_x, new_y):
                            # print(
                            #     f"Znaleziono alternatywna pozycje ({new_x}, {new_y}) zamiast ({preferred_x}, {preferred_y})")
                            # self.occ.append((new_x, new_y))
                            return new_x, new_y

        # print(f"Nie znaleziono alternatywnej pozycji dla ({preferred_x}, {preferred_y}) w promieniu {max_offset}")
        return None, None

    def get_town_type(self, x: int, y: int) -> int:
        num: int = x + y * self.map_format
        tile_type = TerrainType(self.tiles[num].terrain_type)

        def getTownType(chances: list[int]):
            r = randint(1, sum(chances))
            for i in range(0, len(chances)):
                # print(i, r, sum(chances[:i + 1]), )
                if r <= sum(chances[:i + 1]):
                    # print(i, TownType(i).name)
                    return i

        if tile_type == TerrainType.DIRT:
            return getTownType([0, 0, 0, 0, 2, 1, 0, 0, 0])
        elif tile_type == TerrainType.SAND:
            return getTownType([1, 1, 1, 1, 1, 1, 1, 1, 1])
        elif tile_type == TerrainType.GRASS:
            return getTownType([6, 7, 1, 0, 0, 1, 1, 1, 7])
        elif tile_type == TerrainType.SNOW:
            return getTownType([0, 0, 1, 0, 0, 0, 0, 0, 0])
        elif tile_type == TerrainType.SWAMP:
            return getTownType([0, 0, 0, 0, 0, 0, 0, 1, 0])
        elif tile_type == TerrainType.ROUGH:
            return getTownType([0, 0, 0, 0, 0, 0, 8, 0, 1])
        elif tile_type == TerrainType.SUBTERRANEAN:
            return getTownType([0, 0, 3, 4, 8, 4, 0, 2, 0])
        elif tile_type == TerrainType.LAVA:
            return getTownType([0, 0, 0, 1, 0, 0, 0, 0, 0])
        else:
            raise Exception(f"Nieobslugiwany typ terenu: {tile_type}")

    def find_city_position(self, fields_info, main_field_id, all_regions):
        main_field = next((f for f in fields_info if f.field_id == main_field_id), None)
        if not main_field:
            return None, None

        # City position: pick a tile that belongs to the main field (closest to centroid)
        region_obj = next((r for r in all_regions if r.region_id == main_field_id), None)
        if region_obj and getattr(region_obj, 'tiles', None):
            cx, cy = main_field.centroid
            tile_x, tile_y = min(region_obj.tiles, key=lambda t: (t[0] + 0.5 - cx) ** 2 + (t[1] + 0.5 - cy) ** 2)
            # precise center is the tile center (0.5 accuracy)
            return tile_x + 0.5, tile_y + 0.5
        else:
            # fallback to precise centroid rounded to 0.5
            return round(main_field.centroid[0] * 2) / 2, round(main_field.centroid[1] * 2) / 2

    def generate_cities_precise_positioning(self):
        """
        Generate cities with precise positioning using exact geometric centers (to 0.5 grid accuracy).
        Cities are placed at exact centroids, RandomDwellings at exact centroids of additional fields.
        """

        city_positions = self.result["cities"]
        all_regions = self.result["all_regions"]
        city_to_fields = self.result["city_to_fields"]
        fields_info = self.result["fields_info"]

        cities = []
        cities_templates = []
        id = self.id
        absod_id = self.absod_id

        try:
            # Create cities and random dwellings based on precise field centroids
            for i, pos in enumerate(city_positions):
                # Get fields assigned to this city
                assigned_fields = city_to_fields.get(i, [])
                if len(assigned_fields) < 1:
                    continue

                # Main field is the first in the list
                main_field_id = assigned_fields[0]

                # Find information about the main field
                precise_city_x, precise_city_y = self.find_city_position(fields_info, main_field_id, all_regions)
                if precise_city_x == None or precise_city_y == None:
                    continue

                city_x = int(precise_city_x)  # For grid validation
                city_y = int(precise_city_y)  # For grid validation

                town_type_index = self.get_town_type(city_x, city_y)
                town_template = self.towns[town_type_index]

                # Sprobuj znajsc dobra pozycje dla miasta
                final_city_x, final_city_y = self.find_alternative_position(town_template, city_x, city_y, max_offset=5)

                if final_city_x is not None and final_city_y is not None:
                    id = id + 1
                    absod_id = absod_id + 1

                    cities_templates.append(town_template)
                    cities.append(Objects(final_city_x, final_city_y, 0, id, [],
                                          Town(absod_id, i, None, None, Formation.SPREAD, None, 1,
                                               MustHaveSpell.create_default(), MayNotHaveSpell.create_default(), [],
                                               255, [])))
                    self.final_city_positions.append((town_type_index, final_city_x, final_city_y))

                    # Oznacz kafelki miasta jako zajete
                    tmp: ObjectsTemplate = copy(town_template)
                    tmp.passability = [7 for _ in range(6)]
                    self.players[i].main_town = MainTown(0, town_type_index, final_city_x - 2, final_city_y, 0)
                    self.mark_object_tiles_as_occupied(tmp, final_city_x, final_city_y, 3)

            self.objectTemplates.extend(cities_templates)
            self.objects.extend(cities)

            self.id = id
            self.absod_id = absod_id

            # Wyswietl statystyki zajetosci mapy
            # self.print_occupation_stats()

        except Exception as e:
            print(f"Error generating cities with precise positioning: {e}")
            raise e

    def find_dwelling_position(self, all_regions, additional_field_id, additional_field):
        # Precise dwelling position: pick a tile inside the field (closest to centroid)
        add_region = next((r for r in all_regions if r.region_id == additional_field_id), None)
        if add_region and getattr(add_region, 'tiles', None):
            acx, acy = additional_field.centroid
            d_tile_x, d_tile_y = min(add_region.tiles,
                                     key=lambda t: (t[0] + 0.5 - acx) ** 2 + (t[1] + 0.5 - acy) ** 2)
            return d_tile_x + 0.5, d_tile_y + 0.5
        else:
            return round(additional_field.centroid[0] * 2) / 2, round(additional_field.centroid[1] * 2) / 2

    def get_city_type(self, i):
        objectTemplate: ObjectsTemplate = self.objectTemplates[i + 2]
        for i, city in enumerate(self.towns):
            if objectTemplate == city:
                return i
        return None

    def generate_dwelling_precise_positioning(self):
        city_positions = self.result["cities"]
        all_regions = self.result["all_regions"]
        city_to_fields = self.result["city_to_fields"]
        fields_info = self.result["fields_info"]

        dwellings = []
        dwelling_templates = []
        id = self.id
        absod_id = self.absod_id

        for i, pos in enumerate(city_positions):
            # Get fields assigned to this city
            assigned_fields = city_to_fields.get(i, [])
            if len(assigned_fields) < 1:
                continue
            # Add RandomDwelling on remaining fields with precise positioning
            for additional_field_id in assigned_fields[1:]:  # Skip first field (main)
                additional_field = next((f for f in fields_info if f.field_id == additional_field_id), None)
                if additional_field:
                    precise_dwelling_x, precise_dwelling_y = self.find_dwelling_position(all_regions,
                                                                                         additional_field_id,
                                                                                         additional_field)
                    dwelling_x = int(precise_dwelling_x)  # For grid validation
                    dwelling_y = int(precise_dwelling_y)  # For grid validation

                    # Use template for random dwelling odpowiadaj�cego typowi miasta
                    town_type_index, _, _ = self.final_city_positions[i]
                    dwelling_template = self.dwellings_random[town_type_index] if town_type_index < len(
                        self.dwellings_random) else self.dwellings_random[0]

                    # Sprobuj znajsc dobra pozycje dla dwelling
                    final_dwelling_x, final_dwelling_y = self.find_alternative_position(dwelling_template, dwelling_x,
                                                                                        dwelling_y, max_offset=3)

                    if final_dwelling_x is not None and final_dwelling_y is not None:
                        id = id + 1
                        absod_id = absod_id + 1
                        dwelling_templates.append(dwelling_template)
                        dwellings.append(Objects(final_dwelling_x, final_dwelling_y, 0, id, [],
                                                 RandomDwellingPresetAlignment.create_default()))

                        # Oznacz kafelki dwelling jako zajete
                        self.mark_object_tiles_as_occupied(dwelling_template, final_dwelling_x, final_dwelling_y, 2)

        self.objectTemplates.extend(dwelling_templates)
        self.objects.extend(dwellings)

        self.id = id
        self.absod_id = absod_id


    def generate_heroes_positioning(self):
        heroes = []
        heroes_templates = []
        id = self.id
        absod_id = self.absod_id

        for i, (city, pos_x, pos_y) in enumerate(self.final_city_positions):
            a = randint(0, 1)
            # print(f"Hero city {i}: {city} ({pos_x}, {pos_y}): {city * 2 + a}")
            heroTemplate = self.heroes[city * 2 + a]
            type = (city * 2 + a) * 8 + randint(0, 7)
            hero: Objects = self.heroes_specification[type]

            final_x, final_y = self.find_alternative_position(heroTemplate, pos_x, pos_y, max_offset=5, validation_function=self.validate_placement_for_landscape)

            if final_x is not None and final_y is not None:
                id = id + 1
                absod_id = absod_id + 1

                hero.x = final_x
                hero.y = final_y
                hero.template_idx = id
                hero.properties['absod_id'] = absod_id
                hero.properties['type'] = type
                hero.properties['owner'] = i

                heroes_templates.append(heroTemplate)
                heroes.append(hero)
                self.players[i].can_be_computer = 1
                self.players[i].can_be_human = 1
                self.players[i].starting_hero.type = type
                self.players[i].starting_hero.portrait = type
                self.players[i].heroes = [Heroes(type, '')] #HeroEnum(type).name
                if city == 0: self.players[i].allowed_alignments.castle = True
                elif city == 1: self.players[i].allowed_alignments.rampart = True
                elif city == 2: self.players[i].allowed_alignments.tower = True
                elif city == 3: self.players[i].allowed_alignments.inferno = True
                elif city == 4: self.players[i].allowed_alignments.necropolis = True
                elif city == 5: self.players[i].allowed_alignments.dungeon = True
                elif city == 6: self.players[i].allowed_alignments.stronghold = True
                elif city == 7: self.players[i].allowed_alignments.fortress = True
                elif city == 8: self.players[i].allowed_alignments.conflux = True

                self.mark_object_tiles_as_occupied(heroTemplate, final_x, final_y)

        self.objectTemplates.extend(heroes_templates)
        self.objects.extend(heroes)

        self.id = id
        self.absod_id = absod_id


    def generate_special_building(self):
        self.generate_special_building_level3()
        self.generate_special_building_level2()
        self.generate_special_building_level1_5()
        self.generate_special_building_level1()

    def generate_special_building_level1(self):
        fields_info = self.result['fields_info']
        special_buildings = read_object_templates_from_json("special_buildings_level1")

        all_regions = self.result['all_regions']
        city_to_fields = self.result['city_to_fields']
        # tiles_of_5 = get_region_tiles(all_regions, region_id=5)

        buildings_templates = []
        buildings = []

        id = self.id
        absod_id = self.absod_id

        for _, city_fields in city_to_fields.items():
            for field in city_fields:
                for _ in range(randint(1, 2)):
                    r = randint(0, len(special_buildings) - 1)
                    template = special_buildings[r]

                    pos_x, pos_y = sample(get_region_tiles(all_regions, region_id=field), k=1)[0]

                    final_x, final_y = self.find_alternative_position(template, pos_x, pos_y,
                                                                      max_offset=10)

                    if final_x is not None and final_y is not None:
                        id = id + 1

                        if r == 6:
                            object = Objects(final_x, final_y, 0, id, [], WitchHut.create_default())
                        elif r == 9:
                            object = Objects(final_x, final_y, 0, id, [], Shrine.create_default())
                        elif r == 12:
                            object = Objects(final_x, final_y, 0, id, [], Scholar.create_default())
                        elif 13 <= r <= 15:
                            object = Objects(final_x, final_y, 0, id, [], SeersHut.create_default())
                        else:
                            object = Objects(final_x, final_y, 0, id, [], None)
                        # print(f"Lv1 ({final_x, final_y})")
                        buildings_templates.append(template)
                        buildings.append(object)

                        self.mark_object_tiles_as_occupied(template, final_x, final_y, 3)

        self.objectTemplates.extend(buildings_templates)
        self.objects.extend(buildings)

        self.id = id
        self.absod_id = absod_id



    def generate_special_building_level1_5(self):
        special_buildings = [(i,j) for i,j in zip(read_object_templates_from_json("special_buildings_level1.5"), read_object_from_json("special_buildings_level1.5"))]
        default_special_building = special_buildings[:2]
        dirt_building = default_special_building + special_buildings[2:15]
        sand_building = default_special_building + special_buildings[15:25]
        grass_building = default_special_building + special_buildings[25:41]
        snow_building = default_special_building + special_buildings[41:52]
        swamp_building = default_special_building + special_buildings[52:65]
        rough_building = default_special_building + special_buildings[65:76]
        subterranean_building = default_special_building + special_buildings[76:85]
        lava_building = default_special_building + special_buildings[85:]
        buildings_obj = [dirt_building, sand_building, grass_building, snow_building, swamp_building, rough_building, subterranean_building, lava_building]

        buildings_templates = []
        buildings = []

        id = self.id
        absod_id = self.absod_id

        city_to_fields = self.result['city_to_fields']
        fields_info = self.result['fields_info']

        for _, city_fields in city_to_fields.items():
            for field_number in city_fields[1:2]:
                boundary_raster = fields_info[field_number - 1].boundary_raster
                chosen_boundary_raster = choices(boundary_raster, k=randint(1, 2))

                object_class = []
                for pos_x, pos_y in chosen_boundary_raster:
                    test_template = ObjectsTemplate.create_default()
                    test_template.passability = [255, 255, 255, 248, 248, 240]
                    final_x, final_y = self.find_alternative_position(test_template, pos_x, pos_y,
                                                                      max_offset=10)
                    if final_x is not None and final_y is not None:
                        num: int = final_x + final_y * self.map_format
                        tile_type: int = self.tiles[num].terrain_type
                        if tile_type < 8:
                            template, object = sample(buildings_obj[tile_type], k=1)[0]
                            if template.object_class not in object_class:
                                id = id + 1

                                object.template_idx = id
                                object.x = final_x
                                object.y = final_y
                                # print(f"Lv1.5 ({final_x, final_y})")
                                buildings_templates.append(template)
                                buildings.append(object)

                                self.mark_object_tiles_as_occupied(template, final_x, final_y, 3)
                                # object_class.append(l[0].object_class)

        self.objectTemplates.extend(buildings_templates)
        self.objects.extend(buildings)

        self.id = id
        self.absod_id = absod_id


        #         # trzeba upewnc sie, ze wylowowane obiekty, nawet jezeli sa z roznych terrain type, maja byc roznego typu
        #         # tzn. nie chce miec ore mine z dirtu i z sand itp



    def generate_special_building_level2(self):
        special_buildings_templates = read_object_templates_from_json("special_buildings_level2")
        terrain_buildings_partition = [(20, 27), (28, 30), (31, 36), (37, 40), (41, 44), (45, 49), (50, 50), (51, 52)]
        empty_regions = self.get_regions_without_cities()
        fields_info = self.result['fields_info']

        buildings = []
        buildings_templates = []
        id = self.id

        for region in empty_regions:
            boundary_raster = fields_info[region].boundary_raster
            chosen_boundary_raster = choices(boundary_raster, k=randint(1, 2))
            for pos_x, pos_y in chosen_boundary_raster:
                test_template = ObjectsTemplate.create_default()
                test_template.passability = [255, 255, 248, 240, 240, 248]
                final_x, final_y = self.find_alternative_position(test_template, int(pos_x), int(pos_y), max_offset=510)

                if final_x is not None and final_y is not None:
                    tile_type_idx: int = TerrainType(self.tiles[final_y * self.map_format + final_x].terrain_type).value
                    if tile_type_idx >= 8:
                        continue
                    lowest, highest = terrain_buildings_partition[tile_type_idx]
                    r = randint(lowest, highest + 20)
                    if r > highest:
                        r = r - highest - 1

                    if r == 6:
                        building = Objects(final_x, final_y, 0, id, [], Shrine.create_default())
                    else:
                        building = Objects(final_x, final_y, 0, id, [], None)

                    id = id + 1
                    building.template_idx = id

                    template = special_buildings_templates[r]
                    # print(f"Lv2 ({final_x, final_y})")
                    buildings_templates.append(template)
                    buildings.append(building)

                    self.mark_object_tiles_as_occupied(template, final_x, final_y, 4)

        self.objectTemplates.extend(buildings_templates)
        self.objects.extend(buildings)

        self.id = id


    def get_regions_without_cities(self):
        tmp = []
        city_to_fields = self.result['city_to_fields']
        for i in city_to_fields.items():
            tmp.extend(i[1])

        return [i - 1 for i in range(1, len(self.result['fields_info'])) if i not in tmp]

    def generate_special_building_level3(self):
        special_buildings_templates = read_object_templates_from_json("special_buildings_level3")
        empty_regions = self.get_regions_without_cities()
        fields_info = self.result['fields_info']

        buildings = []
        buildings_templates = []
        id = self.id
        absod_id = self.absod_id

        for region in empty_regions:
            pos_x, pos_y = fields_info[region].centroid

            r = randint(0, len(special_buildings_templates) - 1)
            template = special_buildings_templates[r]

            final_x, final_y = self.find_alternative_position(template, int(pos_x), int(pos_y), max_offset=10)

            if final_x is not None and final_y is not None:
                id = id + 1

                if r == 0:  # Prison
                    hero = Hero.create_default()
                    hero.type = randint(0, 1)
                    hero.absod_id = absod_id
                    absod_id = absod_id + 1

                    building = Objects(final_x, final_y, 0, id, [], hero)
                elif r == 3:
                    building = Objects(final_x, final_y, 0, id, [], Shrine.create_default())
                else:
                    building = Objects(final_x, final_y, 0, id, [], None)

                building.template_idx = id
                # print(f"Lv3 ({final_x, final_y})")
                buildings_templates.append(template)
                buildings.append(building)

                self.mark_object_tiles_as_occupied(template, final_x, final_y, 4)

        self.objectTemplates.extend(buildings_templates)
        self.objects.extend(buildings)

        self.id = id
        self.absod_id = absod_id


    def find_furtherest_point(self):
        points = []

        for x in range(self.map_format):
            for y in range(self.map_format):
                if self.occupied_tiles[x][y]:
                    points.append((x, y))

        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        dist = [[-1] * self.map_format for _ in range(self.map_format)]

        queue = deque()

        # wrzucamy wszystkie punkty startowe do BFS
        for x, y in points:
            dist[x][y] = 0
            queue.append((x, y))
            # print((x, y))

        # BFS wieloźródłowy
        while queue:
            x, y = queue.popleft()
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 5 <= nx < self.map_format - 5 and 5 <= ny < self.map_format - 5 and dist[nx][ny] == -1:
                    dist[nx][ny] = dist[x][y] + 1
                    queue.append((nx, ny))

        # znajdujemy punkt o maksymalnej minimalnej odległości
        best_x = best_y = -1
        best_dist = -1

        for x in range(self.map_format):
            for y in range(self.map_format):
                if dist[x][y] > best_dist:
                    best_dist = dist[x][y]
                    best_x = x
                    best_y = y

        # for x in range(self.map_format):
        #     print(dist[x])

        return best_y, best_x, best_dist

    def generate_win_lose_condition(self):
        if self.victory_condition_params.victory_condition == VictoryConditions.ACQUIRE_ARTIFACT or self.victory_condition_params.victory_condition == VictoryConditions.TRANSPORT_ARTIFACT:
            pos_x, pos_y, dist = self.find_furtherest_point()
            print(f"win condition {pos_x}, {pos_y}, {dist}")
            r: int = ar_converterTypeToNum(self.victory_condition_params.artifact_type)
            if r <= 9:
                s = "AVA000" + str(r) + ".def"
            elif r <= 99:
                s = "AVA00" + str(r) + ".def"
            elif r <= 127:
                s = "AVA0" + str(r) + ".def"
            else:
                s = "AVA0" + str(r+1) + ".def"
            template = ObjectsTemplate(s, [255, 255, 255, 255, 255, 127], [0, 0, 0, 0, 0, 128],
                                       [255, 1], [255, 0], 5, r, 4, 0)

            final_x, final_y = self.find_alternative_position(template, int(pos_x), int(pos_y), max_offset=10)

            if final_x is not None and final_y is not None:
                self.id = self.id + 1

                self.mark_object_tiles_as_occupied(template, final_x, final_y, 2)

                self.objectTemplates.append(template)
                self.objects.append(Objects(final_x, final_y, 0, self.id, [], Artifact(
                    Guardians("You did not expect, it would be that easy, did you?",
                              [Creatures(0, randint(1, 1)) for _ in range(7)]))))

        elif self.victory_condition_params.victory_condition == VictoryConditions.ACCUMULATE_CREATURES or self.victory_condition_params.victory_condition == VictoryConditions.ACCUMULATE_RESOURCES:
            special_buildings_templates = read_object_templates_from_json("special_buildings_level3")
            empty_regions = self.get_regions_without_cities()
            fields_info = self.result['fields_info']

            boundary_raster = []

            for region in empty_regions:
                boundary_raster.extend(fields_info[region].boundary_raster)

            chosen_boundary_raster = choices(boundary_raster, k=3)

            for pos_x, pos_y in chosen_boundary_raster:
                test_template = ObjectsTemplate.create_default()
                test_template.passability = [255, 255, 248, 240, 240, 248]
                final_x, final_y = self.find_alternative_position(test_template, int(pos_x), int(pos_y), max_offset=510)

                if final_x is not None and final_y is not None:
                    tile_type_idx: int = TerrainType(self.tiles[final_y * self.map_format + final_x].terrain_type).value
                    if tile_type_idx >= 8:
                        continue

                    self.id = self.id + 1

                    if self.victory_condition_params.victory_condition == VictoryConditions.ACCUMULATE_CREATURES:
                        creature = cr_converterTypeToNum(self.victory_condition_params.creature_type)
                        template: ObjectsTemplate = self.dwellings[int(creature / 2)]
                        object: Objects = Objects(final_x, final_y, 0, self.id, [],
                                                 TrivialOwnedObject.create_default())

                    else:
                        print(self.victory_condition_params.resource_type.value)
                        template: ObjectsTemplate = self.mines[tile_type_idx * 7 + self.victory_condition_params.resource_type.value]
                        object: Objects = Objects(final_x, final_y, 0, self.id, [],
                                                  TrivialOwnedObject.create_default())

                    self.objectTemplates.append(template)
                    self.objects.append(object)
                    self.mark_object_tiles_as_occupied(template, final_x, final_y, 3)


        elif self.victory_condition_params.victory_condition == VictoryConditions.BUILD_GRAIL:
            for i in range(randint(5, 8)):
                pos_x, pos_y = randint(1, 70), randint(1, 70)
                test_template = ObjectsTemplate.create_default()
                test_template.passability = [255, 224, 224, 224, 224, 224]
                final_x, final_y = self.find_alternative_position(test_template, int(pos_x), int(pos_y), max_offset=5)
                if final_x is not None and final_y is not None:

                    size = 5

                    x_obelisk, y_obelisk = randint(1, size - 2), randint(1, size - 2)
                    x_monster, y_monster = randint(0, size - 1), randint(0, size - 1)
                    while x_monster == x_obelisk and y_monster == y_obelisk:
                        x_monster, y_monster = randint(0, size - 1), randint(0, size - 1)

                    tab = [['.' for _ in range(size)] for _ in range(size)]
                    tab[x_obelisk][y_obelisk] = 'o'
                    tab[x_monster][y_monster] = 'm'
                    # for i in range(size):
                    #     print(tab[i])
                    # print()

                    # Przykład, . oznacza puste pole, o obelisk, m potwór
                    #
                    #  . . . . .
                    #  . o . . .
                    #  . . . . .
                    #  . . . m .
                    #  . . . . . <- final_x, final_y
                    #
                    # pozycje są względne, względem final_x, final_y; poprzez sądowanie test_template mamy pewność,
                    # że taki kwadrat może zostać postawiony
                    #
                    # taka tablica może zostać obrócona
                    # np. odbicie lustrzane
                    #
                    #  . . . . .
                    #  . . . o .
                    #  . . . . .
                    #  . m . . .
                    #  . . . . . <- final_x, final_y
                    #
                    # chciałbym otrzymać tablicę takich obiektów, żeby obrysować tę parę
                    # nie musi to być kwadrat
                    # np. (t teren/krajobraz)                                   4-y, x
                    #  . . t t t                       . t t . .         . . . . 0,0     4-0, 0
                    #  . t t o t                       . m . t .         . . . . 0,1     4-0, 1
                    #  t . . . t                --->   . t . t t         . . . . 0,2     4-0, 2
                    #  t m t t t                       . t . o t         . . . . 0,3     4-0, 3
                    #  . . . . . <- final_x, final_y   . t t t t         . . . . 0,4     4-0, 4


                    # obrócenie tablicy obiektów
                    # 0 - brak obrotu
                    # 1 - 90 stopni w prawo
                    # 2 - 180 stopni
                    # 3 - 270 stopni w prawo

                    def rotate():
                        return [[tab[size - y - 1][x] for y in range(size)] for x in range(size)]

                    for _ in range(randint(0, 4)):
                        tab = rotate()

                    # for i in range(size):
                    #     print(tab[i])
                    # print()

                    for x in range(size):
                        for y in range(size):
                            if not tab[x][y] == '.':
                                self.id = self.id + 1
                                if tab[x][y] == 'o':
                                    object = Objects(final_x - size + x, final_y - size + y, 0, self.id, [], None)
                                    template: ObjectsTemplate = ObjectsTemplate("AvXOblG.def", [255, 255, 255, 255, 255, 127], [0, 0, 0, 0, 0, 128], [255, 1], [1, 0], 57, 0 , 0, 0)
                                else:
                                    self.absod_id = self.absod_id + 1
                                    monster = Monster(self.absod_id, 82, Disposition.HOSTILE, None, 0, 0)
                                    object = Objects(final_x - size + x, final_y - size + y, 0, self.id, [], monster)
                                    template: ObjectsTemplate = ObjectsTemplate("AVWgobx0.def", [255, 255, 255, 255, 255, 127], [0, 0, 0, 0, 0, 128], [255, 1], [1, 0], 54, 85, 2 ,0)

                                self.objectTemplates.append(template)
                                self.objects.append(object)
                                self.mark_object_tiles_as_occupied(template, final_x - size + x, final_y - size + y)
