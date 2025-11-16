from generation.map_gen.sprite_handlers.SpriteHandler import SpriteHandler
from classes.tile.Tile import TerrainType
from generation.tile_gen.tile_gen import SpriteType, get_terrain_type_sprite_type_range
from random import randint

class SandSpriteHandler(SpriteHandler):
    def choose_sprite(self, terrain_map, x, y) -> tuple[int, bool, bool]:
        allowed_sprite_ranges = get_terrain_type_sprite_type_range(TerrainType.SAND, SpriteType.CENTER)
        if allowed_sprite_ranges["special"] and randint(1, 10) == 1:
            return randint(allowed_sprite_ranges["special"][0], allowed_sprite_ranges["special"][1]), False, False
        
        return randint(allowed_sprite_ranges["standard"][0], allowed_sprite_ranges["standard"][1]), False, False