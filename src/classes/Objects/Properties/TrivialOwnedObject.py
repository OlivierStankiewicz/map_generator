from src.classes.Objects.PropertiesBase import Properties


class TrivialOwnedObject(Properties):
    @classmethod
    def create_default(cls) -> 'TrivialOwnedObject':
        return cls(
            owner= 0,
            unknown= []
        )

    def __init__(self, owner: int, unknown: list[int]) -> None:
        self.owner = owner
        self.unknown = unknown

    def to_dict(self) -> dict:
        return {
            'owner': self.owner,
            'unknown': self.unknown
        }