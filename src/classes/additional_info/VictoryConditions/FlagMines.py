from classes.additional_info.VictoryConditions.Details import Details
from classes.Enums.VictoryConditions import VictoryConditions

class FlagMines(Details):

    @classmethod
    def create_default(cls) -> "FlagMines":
        return cls (
        )

    def __init__(self) -> None:
        pass

    def to_dict(self) -> dict:
        return {}