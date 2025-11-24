from classes.additional_info.VictoryConditions.Details import Details
from classes.Enums.VictoryConditions import VictoryConditions

class FlagDwellings(Details):

    @classmethod
    def create_default(cls) -> "FlagDwellings":
        return cls (
        )

    def __init__(self) -> None:
        pass

    def to_dict(self) -> dict:
        return {}