class Flags:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "Flags":
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

    def __init__(self, terrain_x: bool = False, terrain_y: bool = False, 
                 river_x: bool = False, river_y: bool = False,
                 road_x: bool = False, road_y: bool = False,
                 coast: bool = False, unknown: bool = False) -> None:
        self.terrain_x = terrain_x
        self.terrain_y = terrain_y
        self.river_x = river_x
        self.river_y = river_y
        self.road_x = road_x
        self.road_y = road_y
        self.coast = coast
        self.unknown = unknown

    def to_dict(self) -> dict:
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