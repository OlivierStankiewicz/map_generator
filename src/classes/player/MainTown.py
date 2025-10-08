class MainTown:

    @classmethod
    def create_default(cls) -> "MainTown":
        return cls(
            generate_hero=1, # def: 1
            town_type=0, # TownType
            x=0,
            y=0,
            z=0
        )

    def __init__(self, generate_hero: bool, town_type: int, x: int, y: int, z: int) -> None:
        self.generate_hero = generate_hero
        self.town_type = town_type
        self.x = x
        self.y = y
        self.z = z

    def to_dict(self) -> dict:
        return {
            "generate_hero": self.generate_hero,
            "town_type": self.town_type,
            "x": self.x,
            "y": self.y,
            "z": self.z
        }
