import os
import sys
from copy import copy
from dataclasses import dataclass
from random import randint, choices, sample
from math import sqrt

from shiboken6.Shiboken import Object

from classes.Objects.Properties.Helpers.Artifacts import Artifacts
from classes.Objects.Properties.Helpers.Creatures import Creatures
from classes.Objects.Properties.Helpers.PrimarySkills import PrimarySkills
from classes.Objects.Properties.Helpers.SecondarySkills import SecondarySkills
from classes.Objects.Properties.Helpers.Spells import Spells
from classes.Objects.Properties.Hero import Hero
from classes.Objects.Properties.RandomDwellingPresetAlignment import RandomDwellingPresetAlignment
from classes.Objects.Properties.Shrine import Shrine

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
from generation.object_gen.voronoi_city_placement import generate_city_positions, generate_city_positions_with_fields


@dataclass
class TownParams:
    """Parameters for Town."""
    player_cities: int
    neutral_cities: int
    min_distance: int
    total_regions: int


class ObjectTemplateHelper:
    def __init__(self, tiles: list[Tile], townParams: TownParams, numberOfPlayers: int):
        self.id = 1
        self.absod_id = 0
        self.tiles: list[Tile] = tiles
        self.objectTemplates: list[ObjectsTemplate] = []
        self.objects: list[Objects] = []

        self.towns = read_object_templates_from_json("towns")
        self.dwellings_random = read_object_templates_from_json("random_dwellings")  # 0-8 RANDOM_DWELLING_PRESET_ALIGNMENT; 9 RANDOM_DWELLING; 10 - 16 RANDOM_DWELLING_PRESET_LEVEL
        self.dwellings = read_object_templates_from_json("dwellings")
        self.heroes = read_object_templates_from_json("heroes")
        self.heroes_specification = read_object_from_json("heroes_specification")

        self.map_format = int(sqrt(len(self.tiles) / 2))

        # Tablica dwuwymiarowa do sledzenia zajetych miejsc na mapie
        # True = miejsce zajete/nieprzejezdne, False = miejsce wolne/przejezdne
        self.occupied_tiles = [[False for _ in range(self.map_format)] for _ in range(self.map_format)]
        self.occupied_tiles_excluding_landscape = [[False for _ in range(self.map_format)] for _ in range(self.map_format)]
        self.city_field_mapping = []  # Lista do przechowywania mapowania miast do p�l
        self.final_city_positions: list[tuple[int, int, int]] = [] # TownType.value, pos_x, pos_y

        ### params ###
        self.townParams = townParams
        self.numberOfPlayers = numberOfPlayers


    def initData(self):
        # Generate positions and all regions
        result = generate_city_positions_with_fields(
            self.map_format,
            self.townParams.player_cities,
            self.townParams.neutral_cities,
            self.townParams.min_distance,
            self.townParams.total_regions
        )

        # test = ObjectsTemplate.create_default()
        # test.passability = [255, 255, 255, 255, 255, 254]
        # test.actionability = [0, 0, 0, 0, 0, 0]
        # self.mark_object_tiles_as_occupied(test, 0, 0, 3)

        self.create_default_object_template()
        # warstwa 2 zamki i bohaterowie
        self.generate_cities_precise_positioning(result)
        self.generate_heroes_positioning()
        # warstwa 3 budynki do rekrutacji
        self.generate_dwelling_precise_positioning(result)
        # warstwa 4 budowle specjalne
        self.generate_special_building(result)


        return self.objectTemplates, self.objects, self.city_field_mapping

    def create_default_object_template(self):
        self.objectTemplates.append(ObjectsTemplate.create_default())
        self.objectTemplates.append(
            ObjectsTemplate("AVLholg0.def", [255, 255, 255, 255, 255, 255], [0, 0, 0, 0, 0, 0], [4, 0], [4, 0], 124, 0,
                            0, 1, []))

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
                if not (0 <= tile_x < self.map_format and 0 <= tile_y < self.map_format - 2):
                    if passable or actionable:
                        # obiekt wychodzi poza mapę
                        return False
                    continue

                if passable or actionable:
                    if self.occupied_tiles[tile_y][tile_x]:
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
                            return new_x, new_y

        # print(f"Nie znaleziono alternatywnej pozycji dla ({preferred_x}, {preferred_y}) w promieniu {max_offset}")
        return None, None

    def get_town_type(self, x: int, y: int) -> int:
        num: int = x + y * self.map_format
        tile_type = TerrainType(self.tiles[num].terrain_type)

        def getTownType(chances: list[int]):
            r = randint(1, sum(chances))
            for i in range(0, len(chances)):
                print(i, r, sum(chances[:i + 1]), )
                if r <= sum(chances[:i + 1]):
                    print(i, TownType(i).name)
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

    def generate_cities_precise_positioning(self, result):
        """
        Generate cities with precise positioning using exact geometric centers (to 0.5 grid accuracy).
        Cities are placed at exact centroids, RandomDwellings at exact centroids of additional fields.
        """

        city_positions = result["cities"]
        all_regions = result["all_regions"]
        city_to_fields = result["city_to_fields"]
        fields_info = result["fields_info"]

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
                                          Town(absod_id, 255, None, None, Formation.SPREAD, None, 1,
                                               MustHaveSpell.create_default(), MayNotHaveSpell.create_default(), [],
                                               255, [])))
                    self.final_city_positions.append((town_type_index, final_city_x, final_city_y))

                    # Oznacz kafelki miasta jako zajete
                    tmp: ObjectsTemplate = copy(town_template)
                    tmp.passability = [7 for _ in range(6)]
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

    def generate_dwelling_precise_positioning(self, result):
        city_positions = result["cities"]
        all_regions = result["all_regions"]
        city_to_fields = result["city_to_fields"]
        fields_info = result["fields_info"]

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
            hero: Objects = self.heroes_specification[(city * 2 + a) * 8 + randint(0, 7)]

            final_x, final_y = self.find_alternative_position(heroTemplate, pos_x, pos_y, max_offset=5, validation_function=self.validate_placement_for_landscape)

            if final_x is not None and final_y is not None:
                id = id + 1
                absod_id = absod_id + 1

                hero.x = final_x
                hero.y = final_y
                hero.template_idx = id
                hero.properties['absod_id'] = absod_id
                hero.properties['owner'] = i

                heroes_templates.append(heroTemplate)
                heroes.append(hero)

                self.mark_object_tiles_as_occupied(heroTemplate, final_x, final_y)

        self.objectTemplates.extend(heroes_templates)
        self.objects.extend(heroes)

        self.id = id
        self.absod_id = absod_id


    def generate_special_building(self, result):
        self.generate_special_building_level3(result)
        self.generate_special_building_level2(result)
        self.generate_special_building_level1_5(result)
        self.generate_special_building_level1()

    def generate_special_building_level1(self):
        pass

    def generate_special_building_level1_5(self, result):
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

        city_to_fields = result['city_to_fields']
        fields_info = result['fields_info']

        for _, city_fields in city_to_fields.items():
            for field_number in city_fields[1:2]:
                boundary_raster = fields_info[field_number - 1].boundary_raster
                chosen_boundary_raster = choices(boundary_raster, k=randint(2, 3))

                object_class = []
                for pos_x, pos_y in chosen_boundary_raster:
                    num: int = pos_x + pos_y * self.map_format
                    tile_type: int = self.tiles[num].terrain_type
                    if tile_type < 8:
                        tmp = sample(buildings_obj[tile_type], k=len(chosen_boundary_raster))
                        for template, object in tmp:
                            if template.object_class not in object_class:
                                final_x, final_y = self.find_alternative_position(template, pos_x, pos_y,
                                                                                  max_offset=5)
                                if final_x is not None and final_y is not None:
                                    id = id + 1

                                    object.template_idx = id
                                    object.x = final_x
                                    object.y = final_y

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



    def generate_special_building_level2(self, result):
        special_buildings_templates = read_object_templates_from_json("special_buildings_level2")
        terrain_buildings_partition = [(20, 27), (28, 30), (31, 36), (37, 40), (41, 44), (45, 49), (50, 50), (51, 52)]
        empty_regions = self.get_regions_without_cities(result)
        fields_info = result['fields_info']

        buildings = []
        buildings_templates = []
        id = self.id

        for region in empty_regions:
            boundary_raster = fields_info[region].boundary_raster
            chosen_boundary_raster = choices(boundary_raster, k=randint(2, 3))
            for pos_x, pos_y in chosen_boundary_raster:
                test_template = ObjectsTemplate.create_default()
                test_template.passability = [255, 255, 249, 240, 240, 248]
                final_x, final_y = self.find_alternative_position(test_template, int(pos_x), int(pos_y), max_offset=5)

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

                    print(r, building)

                    id = id + 1
                    building.template_idx = id

                    template = special_buildings_templates[r]

                    buildings_templates.append(template)
                    buildings.append(building)

                    self.mark_object_tiles_as_occupied(template, final_x, final_y, 2)

        self.objectTemplates.extend(buildings_templates)
        self.objects.extend(buildings)

        self.id = id


    def get_regions_without_cities(self, result):
        tmp = []
        city_to_fields = result['city_to_fields']
        for i in city_to_fields.items():
            tmp.extend(i[1])

        return [i - 1 for i in range(1, len(result['fields_info'])) if i not in tmp]

    def generate_special_building_level3(self, result):
        special_buildings_templates = read_object_templates_from_json("special_buildings_level3")
        empty_regions = self.get_regions_without_cities(result)
        fields_info = result['fields_info']

        buildings = []
        buildings_templates = []
        id = self.id
        absod_id = self.absod_id

        for region in empty_regions:
            pos_x, pos_y = fields_info[region].centroid

            r = randint(0, len(special_buildings_templates) - 1)
            template = special_buildings_templates[r]

            final_x, final_y = self.find_alternative_position(template, int(pos_x), int(pos_y), max_offset=5)

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

                buildings_templates.append(template)
                buildings.append(building)

                self.mark_object_tiles_as_occupied(template, final_x, final_y, 3)

        self.objectTemplates.extend(buildings_templates)
        self.objects.extend(buildings)

        self.id = id
        self.absod_id = absod_id



