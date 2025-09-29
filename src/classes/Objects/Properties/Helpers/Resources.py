class Resources:

    @classmethod
    def create_default(cls) -> "Resources":
        return cls(#liczba także może być ujemna
            wood= 0,
            mercury = 0,
            ore = 0,
            sulfur = 0,
            crystal = 0,
            gems = 0,
            gold = 0
        )

    def __init__(self, wood: int,
				mercury: int,
				ore: int,
				sulfur: int,
				crystal: int,
				gems: int,
				gold: int) -> None:
        self.wood = wood
        self.mercury = mercury
        self.ore = ore
        self.sulfur = sulfur
        self.crystal = crystal
        self.gems = gems
        self.gold = gold

    def to_dict(self) -> dict:
        return {
            "wood": self.wood,
            "mercury": self.mercury,
            "ore": self.ore,
            "sulfur": self.sulfur,
            "crystal": self.crystal,
            "gems": self.gems,
            "gold": self.gold
        }
