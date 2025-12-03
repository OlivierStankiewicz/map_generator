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

class RiverType(Enum):
    NONE = 0
    CLEAR = 1
    ICY = 2
    MUDDY = 3
    LAVA = 4
    
class RoadType(Enum):
    NONE = 0
    DIRT = 1
    GRAVEL = 2
    COBBLESTONE = 3
    
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

    def __init__(self, terrain_type: TerrainType = TerrainType.DIRT, terrain_sprite: int = 22,
                 river_type: RiverType = RiverType.NONE, river_sprite: int = 0,
                 road_type: RoadType = RoadType.NONE, road_sprite: int = 0,
                 flags: Flags = Flags.create_default()) -> None:
        self.terrain_type = terrain_type.value
        self.terrain_sprite = terrain_sprite
        self.river_type = river_type.value
        self.river_sprite =  river_sprite
        self.road_type = road_type.value
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