from classes.Enums.SkillsLevel import SkillsLevel

class SecondarySkills:

    @classmethod
    def create_default(cls) -> "SecondarySkills":
        return cls(
            type=0,
            level=0
        )

    def __init__(self, type: int, level: SkillsLevel) -> None:
        self.type = type
        self.level = level

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "level": self.level.value,
        }