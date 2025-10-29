from classes.additional_info.VictoryConditions.Details import Details
from classes.Enums.VictoryConditions import VictoryConditions
from classes.Enums.HallLevel import HallLevel
from classes.Enums.CastleLevel import CastleLevel

class UpgradeTown(Details):
    @classmethod
    def create_default(cls) -> "UpgradeTown":
        return cls(
            allow_normal_win=0,
            applies_to_computer=0,
            x=0,
            y=0,
            z=0,
            hall_level=0, #HallLevel
            castle_level=0 #CastleLevel
        )

    def __init__(self, allow_normal_win: int, applies_to_computer: int, x: int, y: int, z: int,
                 hall_level: HallLevel, castle_level: CastleLevel) -> None:
        super().__init__(allow_normal_win, applies_to_computer, VictoryConditions.UPGRADE_TOWN)
        self.x = x
        self.y = y
        self.z = z
        self.hall_level = hall_level
        self.castle_level = castle_level

    def to_dict(self) -> dict:
        dict = super().to_dict()
        dict.update({
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "hall_level": self.hall_level.value,
            "castle_level": self.castle_level.value
        })
        return dict
