from src.classes.Enums.VictoryConditions import VictoryConditions


class VictoryCondition:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "VictoryCondition":
        return cls(
            type=VictoryConditions.NORMAL,
            details=None # Details.create_default(), jeśli tryb normal - tego nie ma
        )

    def __init__(self, type: int) -> None:
        self.type = type

    def to_dict(self) -> dict:
        return {
            "type": self.type

        }