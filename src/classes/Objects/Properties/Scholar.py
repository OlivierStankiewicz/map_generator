from src.classes.Objects.PropertiesBase import Properties


class Scholar(Properties):
    @classmethod
    def create_default(cls) -> "Scholar":
        return cls(
            reward_type=0,
            reward_value=0,
            unknown=[]
        )

    def __init__(self, reward_type: int, reward_value: int, unknown: list[int]) -> None:
        self.reward_type = reward_type
        self.reward_value = reward_value
        self.unknown = unknown

    def to_dict(self) -> dict:
        return {
            "reward_type": self.reward_type,
            "reward_value": self.reward_value,
            "unknown": self.unknown
        }