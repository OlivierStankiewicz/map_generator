class BasicInfo:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "BasicInfo":
        return cls(
            is_playable= 1, # 0 1
            map_size= 72,
            has_two_levels= 0, # 0 1
            name= "",
            description= "",
            difficulty= 1, # 0 4
            max_hero_level= 0 # max level
        )
    
    def __init__(self, is_playable: int, map_size: int, has_two_levels: int, name: str, description: str, difficulty: int, max_hero_level: int) -> None:
        self.is_playable = is_playable
        self.map_size = map_size
        self.has_two_levels = has_two_levels
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.max_hero_level = max_hero_level

    def to_dict(self) -> dict:
        return {
            "is_playable": self.is_playable,
            "map_size": self.map_size,
            "has_two_levels": self.has_two_levels,
            "name": self.name,
            "description": self.description,
            "difficulty": self.difficulty,
            "max_hero_level": self.max_hero_level
        }