from src.classes.Objects.Properties.Helpers.DetailsReward import Details


class Reward:
    @classmethod
    def create_default(cls) -> "Reward":
        return cls(
            type=0,
            details = Details.create_default(),
            unknown = []
        )

    def __init__(self, type: int, details: Details, unknown: list[int]) -> None:
        self.type = type
        self.details = details
        self.unknown = unknown

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "details": self.details.to_dict(),
            "unknown": self.unknown
        }