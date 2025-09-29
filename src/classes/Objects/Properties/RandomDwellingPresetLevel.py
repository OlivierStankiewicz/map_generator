from src.classes.Objects import Properties
from src.classes.Objects.Properties.Helpers.Alignment import Alignment


class RandomDwellingPresetLevel(Properties):
    @classmethod
    def create_default(cls) -> "RandomDwellingPresetLevel":
        return cls(
            owner=0,
            town_absord_id= 0,
            alignment= Alignment.create_default()
        )

    def __init__(self, owner: int,
                 town_absord_id: int,
                alignment: Alignment) -> None:
        self.owner = owner
        self.town_absord_id = town_absord_id
        self.alignment = alignment

    def to_dict(self) -> dict:
        return {
            "owner": self.owner,
            "town_absord_id": self.town_absord_id,
            "alignment": self.alignment.to_dict()
        }