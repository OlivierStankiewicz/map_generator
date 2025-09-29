from src.classes.Objects import Properties
from src.classes.Objects.Properties.Helpers.Creatures import Creatures


class Garrison(Properties):
    @classmethod
    def create_defaults(cls) -> "Garrison":
        return cls(
            owner= 0,
            unknown= [0, 0, 0],
            creatures= [Creatures.create_default() for _ in range(7)],
            can_remove_units= 1,
            unknown2= [0, 0, 0, 0, 0, 0, 0, 0]
        )

    def __int__(self, owner: int, unknown: list, creatures: list[Creatures], can_remove_units: int, unknown2: list) -> None:
        self.owner = owner
        self.unknown = unknown
        self.creatures = creatures
        self.can_remove_units = can_remove_units
        self.unknown2 = unknown2

    def to_dict(self) -> dict:
        return {
            "owner": self.owner,
            "unknown": self.unknown,
            "creatures": [creature.to_dict() for creature in self.creatures],
            "can_remove_units": self.can_remove_units,
            "unknown2": self.unknown2
        }