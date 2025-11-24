from classes.additional_info.VictoryConditions.Details import Details
from classes.Enums.VictoryConditions import VictoryConditions

class BuildGrail(Details):
    @classmethod
    def create_default(cls) -> "BuildGrail":
        return cls(
            x=0, # jeśli w konkretnym mieście to coordy miasta, a jak nie to 255 wszędzie
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
