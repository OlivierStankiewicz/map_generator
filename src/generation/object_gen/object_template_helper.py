import os
import sys
from copy import copy
from dataclasses import dataclass
from random import randint
from math import sqrt

from shiboken6.Shiboken import Object

from classes.Objects.Properties.RandomDwellingPresetAlignment import RandomDwellingPresetAlignment

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
from generation.object_gen.json_parser import read_object_templates_from_json
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
        self.dwellings_random = read_object_templates_from_json(
            "random_dwellings")  # 0-8 RANDOM_DWELLING_PRESET_ALIGNMENT; 9 RANDOM_DWELLING; 10 - 16 RANDOM_DWELLING_PRESET_LEVEL
        self.dwellings = read_object_templates_from_json("dwellings")

        self.map_format = int(sqrt(len(self.tiles) / 2))

        # Tablica dwuwymiarowa do sledzenia zajetych miejsc na mapie
        # True = miejsce zajete/nieprzejezdne, False = miejsce wolne/przejezdne
        self.occupied_tiles = [[False for _ in range(self.map_format)] for _ in range(self.map_format)]
        self.city_field_mapping = []  # Lista do przechowywania mapowania miast do p�l

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

        self.create_default_object_template()
        self.generate_cities_precise_positioning(result)
        self.generate_dwelling_precise_positioning(result)

        return self.objectTemplates, self.objects, self.city_field_mapping

    def create_default_object_template(self):
        self.objectTemplates.append(ObjectsTemplate.create_default())
        self.objectTemplates.append(
            ObjectsTemplate("AVLholg0.def", [255, 255, 255, 255, 255, 255], [0, 0, 0, 0, 0, 0], [4, 0], [4, 0], 124, 0,
                            0, 1, []))

    def mark_object_tiles_as_occupied(self, template: ObjectsTemplate, x: int, y: int):
        """
        Oznacza kafelki obiektu jako zajete na podstawie passability i actionability.
        
        Args:
            template: Template obiektu zawierajacy passability i actionability
            x, y: Pozycja obiektu na mapie (lewy gorny rog)
        """
        if not template.passability or not template.actionability:
            return

        # ObjectTemplate ma 6 rzedow i 8 kolumn (6x8 matrix)
        # A[5][7] to prawy dolny rog
        rows = 6
        cols = 8

        for row in range(rows):
            for col in range(cols):
                tile_x = x + col
                tile_y = y + row

                # Sprawdz czy kafelek jest w granicach mapy
                if 0 <= tile_x < self.map_format and 0 <= tile_y < self.map_format:
                    # Pobierz bity passability i actionability dla tego kafelka
                    if row < len(template.passability) and col < 8:
                        # Passability: 1 = przejezdne, 0 = nieprzejezdne
                        passable = bool((template.passability[row] >> col) & 1)

                        # Actionability: podobnie jak passability
                        actionable = False
                        if row < len(template.actionability):
                            actionable = bool((template.actionability[row] >> col) & 1)

                        # Oznacz kafelek jako zajety jesli jest nieprzejezdny lub akcjonowalny
                        # (akcjonowalne kafelki sa traktowane jako nieprzejezdne w grze)
                        if not passable or actionable:
                            self.occupied_tiles[tile_y][tile_x] = True

        print(f"Oznaczono kafelki obiektu na pozycji ({x}, {y}) jako zajete")

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
        # Sprawdz czy pozycja jest w granicach mapy
        if x < 0 or x >= self.map_format or y < 0 or y >= self.map_format:
            print(f"Pozycja ({x}, {y}) jest poza granicami mapy {self.map_format}x{self.map_format}")
            return False

        # Sprawdz kolizje z juz zajetymi kafelkami na podstawie passability/actionability
        if template.passability and template.actionability:
            rows = 6
            cols = 8

            for row in range(rows):
                for col in range(cols):
                    tile_x = x + col
                    tile_y = y + row

                    # Sprawdz czy kafelek jest w granicach mapy
                    if 0 <= tile_x < self.map_format and 0 <= tile_y < self.map_format:
                        # Pobierz bity passability i actionability dla tego kafelka
                        if row < len(template.passability) and col < 8:
                            passable = bool((template.passability[row] >> col) & 1)
                            actionable = False
                            if row < len(template.actionability):
                                actionable = bool((template.actionability[row] >> col) & 1)

                            # Sprawdz kolizje tylko dla kafelkow ktore beda zajete przez obiekt
                            if not passable or actionable:
                                if self.occupied_tiles[tile_y][tile_x]:
                                    print(f"Pozycja ({x}, {y}) - kolizja na kafelku ({tile_x}, {tile_y})")
                                    return False

        # Sprawdz, czy na glownej pozycji nie ma juz obiektu (dodatkowa ochrona)
        for obj in self.objects:
            if obj.x == x and obj.y == y:
                print(f"Pozycja ({x}, {y}) jest juz zajeta przez obiekt {obj}")
                return False

        print(f"Pozycja ({x}, {y}) jest w granicach mapy {self.map_format}x{self.map_format} - OK")
        return True

    def find_alternative_position(self, template: ObjectsTemplate, preferred_x: int, preferred_y: int,
                                  max_offset: int = 3) -> tuple:
        """
        Znajduje alternatywna pozycje dla obiektu w poblizu preferowanej pozycji.
        Zwraca (x, y) jesli znajdzie wolne miejsce, lub (None, None) jesli nie.
        """
        # Najpierw sprobuj preferowana pozycje
        if self.validate_placement(template, preferred_x, preferred_y):
            return preferred_x, preferred_y

        # Sprobuj pozycje w coraz wiekszych okreslach wokol preferowanej pozycji
        for offset in range(1, max_offset + 1):
            for dx in range(-offset, offset + 1):
                for dy in range(-offset, offset + 1):
                    if abs(dx) == offset or abs(dy) == offset:  # Tylko krawedzie prostokata
                        new_x = preferred_x + dx
                        new_y = preferred_y + dy

                        if self.validate_placement(template, new_x, new_y):
                            print(
                                f"Znaleziono alternatywna pozycje ({new_x}, {new_y}) zamiast ({preferred_x}, {preferred_y})")
                            return new_x, new_y

        print(f"Nie znaleziono alternatywnej pozycji dla ({preferred_x}, {preferred_y}) w promieniu {max_offset}")
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

                id = id + 1
                absod_id = absod_id + 1
                town_type_index = self.get_town_type(city_x, city_y)
                town_template = self.towns[town_type_index]

                # Sprobuj znajsc dobra pozycje dla miasta
                final_city_x, final_city_y = self.find_alternative_position(town_template, city_x, city_y, max_offset=5)

                if final_city_x is not None and final_city_y is not None:
                    cities_templates.append(town_template)
                    cities.append(Objects(final_city_x, final_city_y, 0, id, [],
                                          Town(absod_id, 0, None, None, Formation.SPREAD, None, 1,
                                               MustHaveSpell.create_default(), MayNotHaveSpell.create_default(), [],
                                               255, [])))

                    # Oznacz kafelki miasta jako zajete
                    tmp: ObjectsTemplate = copy(town_template)
                    tmp.passability = [7 for _ in range(6)]
                    self.mark_object_tiles_as_occupied(tmp, final_city_x, final_city_y)

                    # Save city to fields mapping
            #         city_type = "Gracz" if pos.is_player_city else "Neutralne"
            #         city_number = i + 1
            #
            #         field_info = f"Miasto {city_number} ({city_type}) - pola {assigned_fields}, precyzyjne centrum ({final_city_x:.1f}, {final_city_y:.1f})"
            #         if final_city_x != city_x or final_city_y != city_y:
            #             field_info += f" (przesuniete z {precise_city_x:.1f}, {precise_city_y:.1f})"
            #         self.city_field_mapping.append(field_info)
            #     else:
            #         print(f"UWAGA: Nie mozna umiescic miasta {i+1} - brak miejsca w poblizu pozycji ({city_x},{city_y})")
            #
            # # Add detailed field information
            # self.city_field_mapping.append("")  # Empty line for separation
            # self.city_field_mapping.append("=== PRECISE POSITIONING FIELD INFO ===")
            #
            # for field in fields_info:
            #     status = f"przypisane do miasta {field.assigned_to_city}" if field.assigned_to_city else "niezalezne"
            #     centroid_str = f"({field.centroid[0]:.2f}, {field.centroid[1]:.2f})"
            #     precise_centroid_x = round(field.centroid[0] * 2) / 2
            #     precise_centroid_y = round(field.centroid[1] * 2) / 2
            #     precise_str = f"precyzyjny ({precise_centroid_x:.1f}, {precise_centroid_y:.1f})"
            #     boundary_count = len(field.boundary)
            #
            #     info = f"Pole {field.field_id}: centrum {centroid_str} -> {precise_str}, powierzchnia {field.area} tiles, {status}"
            #     self.city_field_mapping.append(info)

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

                    id = id + 1
                    absod_id = absod_id + 1

                    # Use template for random dwelling odpowiadaj�cego typowi miasta
                    town_type_index = self.get_city_type(i)
                    dwelling_template = self.dwellings_random[town_type_index] if town_type_index < len(
                        self.dwellings_random) else self.dwellings_random[0]

                    # Sprobuj znajsc dobra pozycje dla dwelling
                    final_dwelling_x, final_dwelling_y = self.find_alternative_position(dwelling_template, dwelling_x,
                                                                                        dwelling_y, max_offset=3)

                    if final_dwelling_x is not None and final_dwelling_y is not None:
                        dwelling_templates.append(dwelling_template)
                        dwellings.append(Objects(final_dwelling_x, final_dwelling_y, 0, id, [],
                                                 RandomDwellingPresetAlignment.create_default()))

                        # Oznacz kafelki dwelling jako zajete
                        self.mark_object_tiles_as_occupied(dwelling_template, final_dwelling_x, final_dwelling_y)

                    #     position_info = f"({final_dwelling_x:.1f}, {final_dwelling_y:.1f})"
                    #     if final_dwelling_x != dwelling_x or final_dwelling_y != dwelling_y:
                    #         position_info += f" (przesuniete z {precise_dwelling_x:.1f}, {precise_dwelling_y:.1f})"
                    #
                    #     print(
                    #         f"Precise RandomDwelling typu {TownType(town_type_index).name} for city {city_number} on field {additional_field_id} at {position_info}")
                    # else:
                    #     print(
                    #         f"UWAGA: Nie mozna umiescic RandomDwelling dla miasta {city_number} na polu {additional_field_id} - brak miejsca")

        self.objectTemplates.extend(dwelling_templates)
        self.objects.extend(dwellings)

    # def generate_heroes_positioning(self):
    #     for city in self.ob
