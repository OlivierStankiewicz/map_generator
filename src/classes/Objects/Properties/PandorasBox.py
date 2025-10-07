from src.classes.Objects.PropertiesBase import Properties
from src.classes.Objects.Properties.Helpers.Creatures import Creatures
from src.classes.Objects.Properties.Helpers.PrimarySkills import PrimarySkills
from src.classes.Objects.Properties.Helpers.Resources import Resources
from src.classes.Objects.Properties.Helpers.SecondarySkills import SecondarySkills
from src.classes.Objects.Properties.Helpers.Spells import Spells


class PandorasBox(Properties):

    @classmethod
    def create_defaults(cls) -> "PandorasBox":
        return cls(
            experience= 0,
            spell_points= 0,
            morale = 0,
            luck = 0,
            resources = Resources.create_default(),
            primary_skills = PrimarySkills.create_default(),
            secondary_skills = [],
            artifacts = [],
            spells = [],
            creatures = [],
            unknown= [0, 0, 0, 0, 0, 0, 0, 0]
            )

    def __int__(self, experience: int,
			spell_points: int,
			morale: int,
			luck: int,
            resources: Resources,
            primary_skills: PrimarySkills,
            secondary_skills: list[SecondarySkills],
            artifacts: list[int],
            spells: list[int],
            creatures: list[Creatures],
            unknown: list[int]) -> None:
        self.experience= experience
        self.spell_points= spell_points
        self.morale= morale
        self.luck= luck
        self.resources= resources
        self.primary_skills= primary_skills
        self.secondary_skills= secondary_skills
        self.artifacts= artifacts
        self.spells= spells
        self.creatures= creatures
        self.unknown= unknown

    def to_dict(self) -> dict:
        return {
            'spell_points' : self.spell_points,
            'morale': self.morale,
            'luck': self.luck,
            'resources' : self.resources.to_dict(),
            'primary_skills' : self.primary_skills.to_dict(),
            'secondary_skills' : [secondary_skill.to_dict() for secondary_skill in self.secondary_skills],
            'artifacts' : self.artifacts,
            'spells' : self.spells,
            'creatures' : [creature.to_dict() for creature in self.creatures],
            'unknown' : self.unknown
        }