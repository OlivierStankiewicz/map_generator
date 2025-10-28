import os
import sys
from dataclasses import dataclass
from random import randint
from math import sqrt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from classes.Objects.Objects import Objects

from classes.Enums.Formation import Formation
from classes.Enums.TownType import TownType
from classes.Objects.Properties.Helpers.MayNotHaveSpell import MayNotHaveSpell
from classes.Objects.Properties.Helpers.MustHaveSpell import MustHaveSpell
from classes.Objects.Properties.Town import Town
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
    def __init__(self, tiles: list[Tile], townParams: TownParams):
        self.id = 1
        self.absod_id = 0
        self.tiles: list[Tile] = tiles
        self.objectTemplates: list[ObjectsTemplate] = []
        self.objects:list[Objects] = []

        self.towns = read_object_templates_from_json("towns")
        dwellings = read_object_templates_from_json("dwellings")
        self.dwellings_random = dwellings[7::8]
        self.dwellings = self.get_dwellings(dwellings)

        self.map_format = int(sqrt(len(self.tiles)/2))

        ### params ###
        self.townParams = townParams
        self.city_field_mapping = []  # Lista do przechowywania mapowania miast do pól


    def get_dwellings(self, dwellings):
        dwel = [[], [], [], [], [], [], [], [], []]
        exclude = [7, 15, 23, 31, 39, 47, 55, 63, 71]
        for i in range(0, len(dwellings)):
            if i not in exclude:
                dwel[int(i / 8)].append(dwellings[i])
        return dwel


    def create_default_object_template(self):
        self.objectTemplates.append(ObjectsTemplate.create_default())
        self.objectTemplates.append(ObjectsTemplate("AVLholg0.def", [255, 255, 255, 255, 255, 255], [0, 0, 0, 0, 0, 0], [4, 0], [4, 0], 124, 0, 0, 1, []))


    def validate_placement(self, template: ObjectsTemplate, x: int, y: int) -> bool:
        # Sprawdz czy pozycja jest w granicach mapy
        if x < 0 or x >= self.map_format or y < 0 or y >= self.map_format:
            print(f"Pozycja ({x}, {y}) jest poza granicami mapy {self.map_format}x{self.map_format}")
            return False
        
        print(f"Pozycja ({x}, {y}) jest w granicach mapy {self.map_format}x{self.map_format} - OK")
        return True


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


    def generate_cities(self):
        # Generuj pozycje miast i wszystkich regionów
        result = generate_city_positions_with_fields(
            self.map_format, 
            self.townParams.player_cities, 
            self.townParams.neutral_cities, 
            self.townParams.min_distance,
            self.townParams.total_regions
        )

        city_positions = result["cities"]
        all_regions = result["all_regions"]  # Lista wszystkich regionów Voronoi
        city_to_fields = result["city_to_fields"]  # Mapowanie miasto -> 3 pola
        fields_info = result["fields_info"]  # Szczegolowe informacje o polach

        cities = []
        cities_templates = []
        id = self.id
        absod_id = self.absod_id

        try:
            # Twórz miasta na podstawie pozycji
            for i, pos in enumerate(city_positions):
                id = id + 1
                absod_id = absod_id + 1
                x = int(pos.x)
                y = int(pos.y)
                town_template = self.towns[self.get_town_type(x, y)]

                if self.validate_placement(town_template, x, y):
                    cities_templates.append(town_template)
                    cities.append(Objects(x, y, 0, id, [],
                                         Town(absod_id, 0, None, None, Formation.SPREAD, None,1,
                                              MustHaveSpell.create_default(), MayNotHaveSpell.create_default(), [], 255, [])))

                    # Zapisz mapowanie miasta do pól
                    city_type = "Gracz" if pos.is_player_city else "Neutralne"
                    city_number = i + 1
                    assigned_fields = city_to_fields.get(i, [])

                    field_info = f"Miasto {city_number} ({city_type}) - pola {assigned_fields}"
                    self.city_field_mapping.append(field_info)
                else:
                    raise Exception(f"Incorrect position of the city ({x},{y})")

            # Dodaj szczegolowe informacje o polach
            self.city_field_mapping.append("")  # Pusta linia dla separacji
            self.city_field_mapping.append("=== SZCZEGOLOWE INFORMACJE O POLACH ===")

            for field in fields_info:
                status = f"przypisane do miasta {field.assigned_to_city}" if field.assigned_to_city else "niezalezne"
                centroid_str = f"({field.centroid[0]:.2f}, {field.centroid[1]:.2f})"
                boundary_count = len(field.boundary)

                info = f"Pole {field.field_id}: centrum {centroid_str}, powierzchnia {field.area} tiles, krawedzi {boundary_count}, {status}"
                self.city_field_mapping.append(info)

                # Dodaj informacje o rasteryzowanych krawêdziach (dyskretne punkty grid'a)
                if hasattr(field, 'boundary_raster') and field.boundary_raster:
                    raster_count = len(field.boundary_raster)
                    self.city_field_mapping.append(f"    Punkty krawedzi na gridzie: {raster_count} punktow")

                    # Pokaz pierwsze kilka punktow rasteryzowanych dla sprawdzenia
                    if raster_count <= 50:  # Pokaz wszystkie jesli niewiele
                        raster_str = ", ".join([f"({p[0]},{p[1]})" for p in field.boundary_raster[:15]])
                        if raster_count > 15:
                            raster_str += f"... (i {raster_count - 15} wiecej)"
                        self.city_field_mapping.append(f"    Grid punkty: {raster_str}")
                    else:
                        # Dla du¿ych pól pokaz tylko pierwsze i ostatnie punkty
                        first_points = ", ".join([f"({p[0]},{p[1]})" for p in field.boundary_raster[:8]])
                        last_points = ", ".join([f"({p[0]},{p[1]})" for p in field.boundary_raster[-3:]])
                        self.city_field_mapping.append(f"    Grid punkty: {first_points}...{last_points} (lacznie {raster_count})")

                # Opcjonalnie: dodaj pierwsze kilka punktow krawedzi float dla sprawdzenia
                if field.boundary and len(field.boundary) <= 10:  # Pokaz krawedzie tylko dla malych pol
                    boundary_str = ", ".join([f"({p[0]:.1f},{p[1]:.1f})" for p in field.boundary[:5]])
                    if len(field.boundary) > 5:
                        boundary_str += "..."
                    self.city_field_mapping.append(f"    Krawedzie float: {boundary_str}")

            self.objectTemplates.extend(cities_templates)
            self.objects.extend(cities)
        except Exception as ex:
            print(ex)
            print("Generating cities again...")
            self.generate_cities()


    def initData(self):
        self.create_default_object_template()
        self.generate_cities()

        return self.objectTemplates, self.objects, self.city_field_mapping


if __name__ == "__main__":
    dwellings = read_object_templates_from_json("dwellings")
    dwell = []
    # get_dwellings(dwellings)
    print(1)
    for i in range(0, 10):
        print(7 + 8 * i)








