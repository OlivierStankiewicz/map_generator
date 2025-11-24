from classes.Enums.VictoryConditions import VictoryConditions
from classes.additional_info.VictoryConditions.Details import Details

class VictoryCondition:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "VictoryCondition":
        return cls(
            type=VictoryConditions.NORMAL, # Details.create_default(), if mode = normal - it doesn't exist

            allow_normal_win = 0,  # def: raczej 1
            applies_to_computer = 0,  # def: idk
            details = None
        )

    def __init__(self, type: VictoryConditions, allow_normal_win: int, applies_to_computer: int, details: Details) -> None:
        self.type = type
        self.allow_normal_win = allow_normal_win
        self.applies_to_computer = applies_to_computer
        self.details = details

    def to_dict(self) -> dict:
        dict = {
            "type": self.type.value
        }
        if self.details is not None and self.type != VictoryConditions.NORMAL:
            dict["details"] = self.details.to_dict()
            dict["details"]["allow_normal_win"] = self.allow_normal_win
            dict["details"]["applies_to_computer"] = self.applies_to_computer


        return dict