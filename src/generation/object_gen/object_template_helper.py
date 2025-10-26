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
from generation.object_gen.voronoi_city_placement import generate_city_positions

@dataclass
class TownParams:
    """Parameters for Town."""
    player_cities: int
    neutral_cities: int
    min_distance: int

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


    # czy colidery się nie nakładają (passability), czy jest dojście do actionability, czy nie jest to tile z wodą
    # lub +- 1 kratka od wody (z wyjątkiem ship wrecków)
    # nie tyczy się obiektów wodnych, dla nich trzeba zrobić inny validator
    def validate_placement(self, template: ObjectsTemplate, x: int, y: int) -> bool:
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
            raise Exception("Incorrect terrain type (probably water/rock)")


    def generate_cities(self):
        # TODO niepowtarzanie templatów
        # TODO dodać generowanie podziemi
        # TODO przydzielanie do graczy
        result = generate_city_positions(self.map_format, self.townParams.player_cities, self.townParams.neutral_cities, self.townParams.min_distance)

        positions = result.cities

        cities = []
        cities_templates = []
        id = self.id
        absod_id = self.absod_id

        # try:
        for pos in positions:
            id = id + 1
            absod_id = absod_id + 1
            x = pos.x
            y = pos.y
            town_template = self.towns[self.get_town_type(x, y)]

            if self.validate_placement(town_template, x, y):
                cities_templates.append(town_template)
                cities.append(Objects(x, y, 0, id, [],
                                     Town(absod_id, 0, None, None, Formation.SPREAD, None,1,
                                          MustHaveSpell.create_default(), MayNotHaveSpell.create_default(), [], 255, [])))
            else:
                raise Exception(f"Incorrect position of the city ({x},{y})")

        self.objectTemplates.extend(cities_templates)
        self.objects.extend(cities)
        # except Exception as ex:
        #     print(ex)
        #     print("Generating cities again...")
        #     self.generate_cities()


    def initData(self):
        self.create_default_object_template()
        self.generate_cities()

        return self.objectTemplates, self.objects


if __name__ == "__main__":
    dwellings = read_object_templates_from_json("dwellings")
    dwell = []
    # get_dwellings(dwellings)
    print(1)
    for i in range(0, 10):
        print(7 + 8 * i)








