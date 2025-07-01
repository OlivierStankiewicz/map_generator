class VictoryCondition:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "VictoryCondition":
        return cls(
            type=255
        )

    def __init__(self, type: int) -> None:
        self.type = type

    def to_dict(self) -> dict:
        return {
            "type": self.type
        }