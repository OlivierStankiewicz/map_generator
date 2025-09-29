from src.classes.Objects import Properties
from src.classes.Objects.Properties.Helpers.Alignment import Alignment


class RandomDwelling(Properties):

    @classmethod
    def create_default(cls) -> "RandomDwelling":
        return cls(
            owner= 0,
            town_absord_id = 0,
            alignment = Alignment.create_default(),
            min_level = 0,
            max_level = 0
        )

    def __init__(self, owner: int,
                town_absord_id: int,
                alignment: Alignment,
                min_level: int,
                max_level: int) -> None:
        self.owner = owner
        self.town_absord_id = town_absord_id
        self.alignment = alignment
        self.min_level = min_level
        self.max_level = max_level

    def to_dict(self) -> dict:
        return {
            "owner": self.owner,
            "town_absord_id": self.town_absord_id,
            "alignment": self.alignment.to_dict(),
            "min_level": self.min_level,
            "max_level": self.max_level
        }