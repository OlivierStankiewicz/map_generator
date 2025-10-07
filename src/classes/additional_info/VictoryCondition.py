from src.classes.Enums.VictoryConditions import VictoryConditions
from src.classes.additional_info.VictoryConditions.Details import Details


class VictoryCondition:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "VictoryCondition":
        return cls(
            type=VictoryConditions.NORMAL,
            details=None # Details.create_default(), jeśli tryb normal - tego nie ma
        )

    def __init__(self, type: VictoryConditions, details: Details) -> None:
        self.type = type

    def to_dict(self) -> dict:
        return {
            "type": self.type.value
        }