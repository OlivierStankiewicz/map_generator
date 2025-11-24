from classes.additional_info.VictoryConditions.Details import Details
from classes.Enums.VictoryConditions import VictoryConditions

class DefeatHero(Details):
    @classmethod
    def create_default(cls) -> "DefeatHero":
        return cls(
            x=0, # coordy bohatera
            y=0,
            z=0
        )

    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z
        }
