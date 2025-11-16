from classes.Enums.SkillsLevel import SkillsLevel

class SecondarySkills:

    @classmethod
    def create_default(cls) -> "SecondarySkills":
        return cls(
            type=0,
            level=SkillsLevel.BASIC
        )

    def __init__(self, type: int, level: SkillsLevel) -> None:
        self.type = type
        self.level = level

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "level": SkillsLevel(self.level).value,
        }