from src.classes.Objects.Properties.Helpers.Creatures import Creatures


class Guardians:

    @classmethod
    def create_default(cls) -> "Guardians":
        return cls(
            message= "",
            creatures= [Creatures.create_default() for _ in range(7)],
            unknown=[0, 0, 0, 0]
        )

    def __init__(self, message: str, creatures: list[Creatures], unknown: list) -> None:
        self.message = message
        self.creatures = creatures
        self.unknown = unknown

    def to_dict(self) -> dict:
        return {
            "message": self.message,
            "creatures": [creature.to_dict() for creature in self.creatures],
            "unknown": self.unknown
        }