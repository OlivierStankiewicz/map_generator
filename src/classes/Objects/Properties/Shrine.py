from src.classes.Objects.PropertiesBase import Properties


class Shrine(Properties):
    @classmethod
    def create_default(cls) -> 'Shrine':
        return cls(
            spell= 0,
            unknown= []
        )

    def __init__(self, spell: int, unknown: list[int]) -> None:
        self.spell = spell
        self.unknown = unknown

    def to_dict(self) -> dict:
        return {
            'spell': self.spell,
            'unknown': self.unknown
        }