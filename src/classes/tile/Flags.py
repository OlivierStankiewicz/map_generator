class Flags:

    # alternative no-argument constructor
    @classmethod
    def create_default(cls):
        return cls(
            terrain_x =  False,
            terrain_y = False,
            river_x = False,
            river_y = False,
            road_x = False,
            road_y = False,
            coast = False,
            unknown = False
        )
    
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