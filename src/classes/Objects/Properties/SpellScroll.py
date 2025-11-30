from classes.Objects.PropertiesBase import Properties

class SpellScroll(Properties):
    @classmethod
    def create_default(cls) -> 'SpellScroll':
        return cls(
            spell= 0
        )

    def __init__(self, spell: int) -> None:
        self.spell = spell
        self.unknown = [0, 0, 0]

    def to_dict(self) -> dict:
        return {
            'spell': self.spell,
            'unknown': self.unknown
        }