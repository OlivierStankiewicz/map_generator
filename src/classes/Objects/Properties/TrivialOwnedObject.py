from classes.Objects.PropertiesBase import Properties

class TrivialOwnedObject(Properties):
    @classmethod
    def create_default(cls) -> 'TrivialOwnedObject':
        return cls(
            owner= 255
        )

    def __init__(self, owner: int) -> None:
        self.owner = owner
        self.unknown = [0, 0, 0]

    def to_dict(self) -> dict:
        return {
            'owner': self.owner,
            'unknown': self.unknown
        }