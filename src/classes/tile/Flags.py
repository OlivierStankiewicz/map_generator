class Flags:
    @classmethod
    def from_default(self):
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