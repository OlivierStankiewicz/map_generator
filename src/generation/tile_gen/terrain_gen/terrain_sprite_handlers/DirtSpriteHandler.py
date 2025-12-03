from generation.tile_gen.terrain_gen.terrain_sprite_handlers.SpriteHandler import SpriteHandler
from classes.tile.Tile import TerrainType
from generation.tile_gen.terrain_gen.terrain_sprite_mappings.sprite_type_dirt import dirt_sprite_mappings
from generation.tile_gen.tile_gen import TerrainSpriteType, get_terrain_type_sprite_type_range
from random import randint

class DirtSpriteHandler(SpriteHandler):
    def __init__(self):
        self.conflict_neighbor_strings = {"NNN\nNNN\nNNX", "NNN\nNNN\nXNN", "NNX\nNNN\nNNN", "XNN\nNNN\nNNN"}
        self.conflict_sprite_mappings = [
            ("NNN\nNNN\nNNX", TerrainSpriteType.SAND_INNER_CORNER, False, False),
            ("NNN\nNNN\nXNN", TerrainSpriteType.SAND_INNER_CORNER, True, False),
            ("NNX\nNNN\nNNN", TerrainSpriteType.SAND_INNER_CORNER, False, True),
            ("XNN\nNNN\nNNN", TerrainSpriteType.SAND_INNER_CORNER, True, True)
        ]

    def choose_sprite(self, terrain_map: list[list[TerrainType]], x: int, y: int) -> tuple[int, bool, bool]:
        neighbors = self._get_neighbors(terrain_map, x, y)
        neighbors_string = self.convert_neighbors_to_string(neighbors)
        if neighbors_string not in dirt_sprite_mappings:
            print("No matching sprite type for neighbors string:", neighbors_string, "at position:", (x, y))
            return 1, False, False

        sprite_type, x_terrain_flip, y_terrain_flip = dirt_sprite_mappings[neighbors_string]
        
        if neighbors_string in self.conflict_neighbor_strings:
            conflict_resolution = self._resolve_inner_corner_conflict(neighbors_string, terrain_map, x, y, self.conflict_sprite_mappings)
            if conflict_resolution:
                sprite_type, x_terrain_flip, y_terrain_flip = conflict_resolution

        allowed_sprite_ranges = get_terrain_type_sprite_type_range(TerrainType.DIRT, sprite_type)
        if allowed_sprite_ranges["special"] and randint(1, 10) == 1:
            return randint(allowed_sprite_ranges["special"][0], allowed_sprite_ranges["special"][1]), x_terrain_flip, y_terrain_flip

        return randint(allowed_sprite_ranges["standard"][0], allowed_sprite_ranges["standard"][1]), x_terrain_flip, y_terrain_flip
    
    def convert_neighbors_to_string(self, neighbors: list[list[TerrainType]]) -> str:
        sand_group = {TerrainType.SAND, TerrainType.ROCK, TerrainType.WATER}
        result = ""
        for row in neighbors:
            for terrain in row:
                if terrain in sand_group:
                    result += "X"
                else:
                    result += "N"
            result += "\n"
        result = result.strip()
        return result