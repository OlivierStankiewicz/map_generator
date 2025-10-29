from classes.Enums.VictoryConditions import VictoryConditions
from classes.additional_info.VictoryConditions.Details import Details

class VictoryCondition:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "VictoryCondition":
        return cls(
            type=VictoryConditions.NORMAL # Details.create_default(), if mode = normal - it doesn't exist
        )

    def __init__(self, type: VictoryConditions) -> None:
        self.type = type
        self.details = Details.create_default()

    def to_dict(self) -> dict:
        return {
            "type": self.type.value
        }