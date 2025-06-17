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

class TileFlags:
    def __init__(self):
        self.terrain_x =  False
        self.terrain_y = False
        self.river_x = False
        self.river_y = False
        self.road_x = False
        self.road_y = False
        self.coast = False
        self.unknown = False
    
    def __init__(self, terrain_x: bool, terrain_y: bool, river_x: bool, river_y: bool, road_x: bool, road_y: bool, coast: bool, unknown: bool):
        self.terrain_x = terrain_x
        self.terrain_y = terrain_y
        self.river_x = river_x
        self.river_y = river_y
        self.road_x = road_x
        self.road_y = road_y
        self.coast = coast
        self.unknown = unknown

    def to_dict(self):
        return {
            "terrain_x": self.terrain_x,
            "terrain_y": self.terrain_y,
            "river_x": self.river_x,
            "river_y": self.river_y,
            "road_x": self.road_x,
            "road_y": self.road_y,
            "coast": self.coast,
            "unknown": self.unknown
        }

class Tile:
    def __init__(self):
        self.terrain_type = TerrainType.WATER
        self.terrain_sprite = 7
        self.river_type = 0
        self.river_sprite =  0
        self.road_type = 0
        self.road_type = 0
        self.flags = TileFlags()

    def __init__(self, terrain_type: TerrainType, terrain_sprite: int, river_type: int, river_sprite: int, road_type: int, road_sprite: int, flags: TileFlags):
        self.terrain_type = terrain_type
        self.terrain_sprite = terrain_sprite
        self.river_type = river_type
        self.river_sprite =  river_sprite
        self.road_type = road_type
        self.road_type = road_sprite
        self.flags = flags

    def to_dict(self):
        return {
            "terrain_type": self.terrain_type,
            "terrain_sprite": self.terrain_sprite,
            "river_type": self.river_type,
            "river_sprite": self.river_sprite,
            "road_type": self.road_type,
            "road_sprite": self.road_sprite,
            "flags": self.flags.to_dict()
        }