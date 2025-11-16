from classes.Objects.PropertiesBase import Properties

class Scholar(Properties):
    @classmethod
    def create_default(cls) -> "Scholar":
        return cls(
            reward_type=255,
            reward_value=0,
        )

    def __init__(self, reward_type: int, reward_value: int) -> None:
        self.reward_type = reward_type
        self.reward_value = reward_value
        self.unknown = [0, 0, 0, 0, 0, 0]

    def to_dict(self) -> dict:
        return {
            "reward_type": self.reward_type,
            "reward_value": self.reward_value,
            "unknown": self.unknown
        }