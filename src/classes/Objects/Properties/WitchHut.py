from src.classes.Objects import Properties


class WitchHut(Properties):
    @classmethod
    def create_default(cls) -> 'WitchHut':
        return cls(
            potential_skills= PotentialSkills.create_default()
        )

    def __init__(self, potential_skills: PotentialSkills) -> None:
        self.potential_skills = potential_skills

    def to_dict(self) -> dict:
        return {
            'potential_skills': self.potential_skills.to_dict()
        }