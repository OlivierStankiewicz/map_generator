from classes.Objects.PropertiesBase import Properties

class Shrine(Properties):
    @classmethod
    def create_default(cls) -> 'Shrine':
        return cls(
            spell= 255,
            unknown= []
        )

    def __init__(self, spell: int, unknown: list[int]) -> None:
        self.spell = spell
        self.unknown = [0, 0, 0]

    def to_dict(self) -> dict:
        return {
            'spell': self.spell,
            'unknown': self.unknown
        }