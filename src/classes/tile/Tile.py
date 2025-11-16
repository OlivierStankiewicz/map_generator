from enum import Enum
from classes.tile.Flags import Flags

class TerrainType(Enum):
    DIRT = 0
    SAND = 1
    GRASS = 2
    SNOW = 3
    SWAMP = 4
    ROUGH = 5
    SUBTERRANEAN = 6
    LAVA = 7
    WATER = 8
    ROCK = 9

class Tile:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "Tile":
        return cls(
            terrain_type = TerrainType.WATER,
            terrain_sprite = 22,
            river_type = 0,
            river_sprite =  0,
            road_type = 0,
            road_sprite = 0,
            flags = Flags.create_default()
        )

    def __init__(self, terrain_type: TerrainType, terrain_sprite: int, river_type: int, river_sprite: int, road_type: int, road_sprite: int, flags: Flags) -> None:
        self.terrain_type = TerrainType(terrain_type).value
        self.terrain_sprite = terrain_sprite
        self.river_type = river_type
        self.river_sprite =  river_sprite
        self.road_type = road_type
        self.road_sprite = road_sprite
        self.flags = flags

    def to_dict(self) -> dict:
        return {
            "terrain_type": self.terrain_type,
            "terrain_sprite": self.terrain_sprite,
            "river_type": self.river_type,
            "river_sprite": self.river_sprite,
            "road_type": self.road_type,
            "road_sprite": self.road_sprite,
            "flags": self.flags.to_dict()
        }