from generation.map_gen.sprite_handlers.SpriteHandler import SpriteHandler
from classes.tile.Tile import TerrainType
from generation.tile_gen.tile_gen import SpriteType, get_terrain_type_sprite_type_range
from generation.map_gen.sprite_mappings.sprite_type_rock import rock_sprite_mappings
from random import randint

class RockSpriteHandler(SpriteHandler):
    def __init__(self):
        self.conflict_neighbor_strings = {"NNN\nNNN\nNNA", "NNN\nNNN\nANN", "NNA\nNNN\nNNN", "ANN\nNNN\nNNN"}
        self.conflict_sprite_mappings = [
            ("NNN\nNNN\nNNA", SpriteType.UPPER_LEFT_INNER_CORNER, False, False),
            ("NNN\nNNN\nANN", SpriteType.UPPER_RIGHT_INNER_CORNER, False, False),
            ("NNA\nNNN\nNNN", SpriteType.LOWER_LEFT_INNER_CORNER, False, False),
            ("ANN\nNNN\nNNN", SpriteType.LOWER_RIGHT_INNER_CORNER, False, False)
        ]

    def choose_sprite(self, terrain_map: list[list[TerrainType]], x: int, y: int) -> tuple[int, bool, bool]:
        neighbors = self._get_neighbors(terrain_map, x, y)
        neighbors_string = self.convert_neighbors_to_string(neighbors)
        if neighbors_string not in rock_sprite_mappings:
            print("No matching sprite type for neighbors string:", neighbors_string, "at position:", (x, y))
            return 1, False, False
        
        sprite_type, x_terrain_flip, y_terrain_flip = rock_sprite_mappings[neighbors_string]
        
        if neighbors_string in self.conflict_neighbor_strings:
            conflict_resolution = self._resolve_inner_corner_conflict(neighbors_string, terrain_map, x, y, self.conflict_sprite_mappings)
            if conflict_resolution:
                sprite_type, x_terrain_flip, y_terrain_flip = conflict_resolution
        
        allowed_sprite_ranges = get_terrain_type_sprite_type_range(TerrainType.ROCK, sprite_type)
        if allowed_sprite_ranges["special"] and randint(1, 10) == 1:
            return randint(allowed_sprite_ranges["special"][0], allowed_sprite_ranges["special"][1]), x_terrain_flip, y_terrain_flip
        
        return randint(allowed_sprite_ranges["standard"][0], allowed_sprite_ranges["standard"][1]), x_terrain_flip, y_terrain_flip