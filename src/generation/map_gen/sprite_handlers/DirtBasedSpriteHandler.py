from generation.map_gen.sprite_handlers.SpriteHandler import SpriteHandler
from classes.tile.Tile import TerrainType
from generation.tile_gen.tile_gen import SpriteType, get_terrain_type_sprite_type_range
from random import randint
from generation.map_gen.sprite_type_dirt_based import dirt_based_terrain_sprite_mappings

class DirtBasedSpriteHandler(SpriteHandler):
    def __init__(self, terrain_type: TerrainType):
        self.terrain_type = terrain_type
        self.sand_conflict_neighbor_strings = {"NNN\nNNN\nNNX", "NNN\nNNN\nXNN", "NNX\nNNN\nNNN", "XNN\nNNN\nNNN"}
        self.sand_conflict_sprite_mappings = [
            ("NNN\nNNN\nNNX", SpriteType.SAND_INNER_CORNER, False, False),
            ("NNN\nNNN\nXNN", SpriteType.SAND_INNER_CORNER, True, False),
            ("NNX\nNNN\nNNN", SpriteType.SAND_INNER_CORNER, False, True),
            ("XNN\nNNN\nNNN", SpriteType.SAND_INNER_CORNER, True, True),
        ]

        self.dirt_conflict_neighbor_strings = {"NNN\nNNN\nNNY", "NNN\nNNN\nYNN", "NNY\nNNN\nNNN", "YNN\nNNN\nNNN"}
        self.dirt_conflict_sprite_mappings = [
            ("NNN\nNNN\nNNY", SpriteType.DIRT_INNER_CORNER, False, False),
            ("NNN\nNNN\nYNN", SpriteType.DIRT_INNER_CORNER, True, False),
            ("NNY\nNNN\nNNN", SpriteType.DIRT_INNER_CORNER, False, True),
            ("YNN\nNNN\nNNN", SpriteType.DIRT_INNER_CORNER, True, True),
        ]

    def choose_sprite(self, terrain_map, x, y) -> tuple[int, bool, bool]:
        neighbors = self._get_neighbors(terrain_map, x, y)
        neighbors_string = self.convert_neighbors_to_string(neighbors)
        if neighbors_string not in dirt_based_terrain_sprite_mappings:
            print("No matching sprite type for neighbors string:", neighbors_string, "at position:", (x, y))
            return 1, False, False

        # sand inner corner conflict
        if neighbors_string in self.sand_conflict_neighbor_strings:
            conflict_resolution = self._resolve_inner_corner_conflict(neighbors_string, terrain_map, x, y, self.sand_conflict_sprite_mappings)
            if conflict_resolution:
                sprite_type, x_terrain_flip, y_terrain_flip = conflict_resolution
                allowed_sprite_ranges = get_terrain_type_sprite_type_range(self.terrain_type, sprite_type)
                if allowed_sprite_ranges["special"] and randint(1, 10) == 1:
                    return randint(allowed_sprite_ranges["special"][0], allowed_sprite_ranges["special"][1]), x_terrain_flip, y_terrain_flip
                
                return randint(allowed_sprite_ranges["standard"][0], allowed_sprite_ranges["standard"][1]), x_terrain_flip, y_terrain_flip

        # dirt inner corner conflict
        if neighbors_string in self.dirt_conflict_neighbor_strings:
            conflict_resolution = self._resolve_inner_corner_conflict(neighbors_string, terrain_map, x, y, self.dirt_conflict_sprite_mappings)
            if conflict_resolution:
                sprite_type, x_terrain_flip, y_terrain_flip = conflict_resolution
                allowed_sprite_ranges = get_terrain_type_sprite_type_range(self.terrain_type, sprite_type)
                if allowed_sprite_ranges["special"] and randint(1, 10) == 1:
                    return randint(allowed_sprite_ranges["special"][0], allowed_sprite_ranges["special"][1]), x_terrain_flip, y_terrain_flip
                return randint(allowed_sprite_ranges["standard"][0], allowed_sprite_ranges["standard"][1]), x_terrain_flip, y_terrain_flip

        sprite_type, x_terrain_flip, y_terrain_flip = dirt_based_terrain_sprite_mappings[neighbors_string]
        
        allowed_sprite_ranges = get_terrain_type_sprite_type_range(self.terrain_type, sprite_type)
        if allowed_sprite_ranges["special"] and randint(1, 10) == 1:
            return randint(allowed_sprite_ranges["special"][0], allowed_sprite_ranges["special"][1]), x_terrain_flip, y_terrain_flip
        return randint(allowed_sprite_ranges["standard"][0], allowed_sprite_ranges["standard"][1]), x_terrain_flip, y_terrain_flip
    
    def convert_neighbors_to_string(self, neighbors: list[list[TerrainType]]) -> str:
        sand_group = {TerrainType.SAND, TerrainType.ROCK, TerrainType.WATER}

        result = ""
        for row in neighbors:
            for terrain in row:
                if terrain == neighbors[1][1]:
                    result += "N"
                elif terrain in sand_group:
                    result += "X"
                else:
                    result += "Y"
            result += "\n"
        result = result.strip()
        return result