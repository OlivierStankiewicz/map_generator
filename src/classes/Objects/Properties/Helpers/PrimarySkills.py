class PrimarySkills:

    @classmethod
    def create_default(cls) -> "PrimarySkills":
        return cls(
            attack= 0,
            defense = 0,
            spell_power = 0,
            knowledge = 0
        )

    def __init__(self, attack: int,
				defense: int,
				spell_power: int,
				knowledge: int) -> None:
        self.attack = attack
        self.defense = defense
        self.spell_power = spell_power
        self.knowledge = knowledge

    def to_dict(self) -> dict:
        return {
            "attack": self.attack,
            "defense": self.defense,
            "spell_power": self.spell_power,
            "knowledge": self.knowledge
        }