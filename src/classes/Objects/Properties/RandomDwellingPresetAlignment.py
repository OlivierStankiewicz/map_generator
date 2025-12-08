from classes.Objects.PropertiesBase import Properties

class RandomDwellingPresetAlignment(Properties):
    @classmethod
    def create_default(cls) -> "RandomDwellingPresetAlignment":
        return cls(
            owner= 255,
            min_level = 0,
            max_level = 4 # 6
        )

    def __init__(self, owner: int,
			min_level: int,
			max_level: int):
        self.owner = owner
        self.min_level = min_level
        self.max_level = max_level

    def to_dict(self) -> dict:
        return {
            "owner": self.owner,
            "min_level": self.min_level,
            "max_level": self.max_level
        }