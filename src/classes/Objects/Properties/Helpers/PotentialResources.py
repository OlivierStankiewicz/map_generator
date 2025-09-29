class PotentialResources:
    @classmethod
    def create_default(cls) -> "PotentialResources":
        return cls(
            wood= False,
            mercury= True,
            ore= True,
            sulfur= True,
            crystal= True,
            gems= True,
            gold= True,
            unknown= False
        )

    def __int__(self, wood: bool, mercury: bool, ore: bool, sulfur: bool, crystal: bool, gems: bool, gold: bool,
                unknown: bool) -> None:
        self.wood = wood
        self.mercury = mercury
        self.ore = ore
        self.sulfur = sulfur
        self.crystal = crystal
        self.gems = gems
        self.gold = gold
        self.unknown = unknown

    def to_dict(self) -> dict:
        return {
            "wood": self.wood,
            "mercury": self.mercury,
            "ore": self.ore,
            "sulfur": self.sulfur,
            "crystal": self.crystal,
            "gems": self.gems,
            "gold": self.gold,
            "unknown": self.unknown
        }
