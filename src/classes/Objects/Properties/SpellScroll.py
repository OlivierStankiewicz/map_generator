from classes.Objects.PropertiesBase import PropertiesType

class SpellScroll(PropertiesType):
    @classmethod
    def create_default(cls) -> 'SpellScroll':
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