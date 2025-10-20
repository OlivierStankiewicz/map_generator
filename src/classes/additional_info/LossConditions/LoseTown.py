from classes.additional_info.LossConditions.Details import Details
from classes.Enums.LossConditions import LossConditions

class LoseTown(Details):
    @classmethod
    def create_default(cls) -> "LoseTown":
        return cls(
            x=0,
            y=0,
            z=0
        )

    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z
        super().__init__(LossConditions.LOSE_TOWN)

    def to_dict(self) -> dict:
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z,
        }
