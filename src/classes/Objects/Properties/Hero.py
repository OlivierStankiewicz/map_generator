from classes.Objects.Properties.Helpers.Artifacts import Artifacts
from classes.Objects.Properties.Helpers.Creatures import Creatures
from classes.Objects.Properties.Helpers.PrimarySkills import PrimarySkills
from classes.Objects.Properties.Helpers.SecondarySkills import SecondarySkills
from classes.Objects.Properties.Helpers.Spells import Spells
from classes.Objects.PropertiesBase import Properties
from classes.additional_info.HeroesAvailability import HeroesAvailability


class Hero(Properties):
    @classmethod
    def create_default(cls) -> 'Hero':
        return cls(
            absod_id = 0,
            owner = 255,
            type = 0,
            name = None,
            experience = None,
            portrait = None,
            secondary_skills = None,
            creatures = None,
            formation = 0,
            artifacts = None,
            patrol_radius = 0,
            biography = None,
            gender = 255,
            spells = None,
            primary_skills = None
        )

    def __init__(self, absod_id: int, owner: int, type: int, name: str, experience: int, portrait: int,
                 secondary_skills: list[SecondarySkills], creatures: list[Creatures], formation: int, artifacts: Artifacts,
                 patrol_radius: int, biography: str, gender: int, spells: Spells, primary_skills: PrimarySkills) -> None:
        self.absod_id = absod_id
        self.owner = owner
        self.type = type
        self.name = name
        self.experience = experience
        self.portrait = portrait
        self.secondary_skills = secondary_skills
        self.creatures = creatures
        self.formation = formation
        self.artifacts = artifacts
        self.patrol_radius = patrol_radius
        self.biography = biography
        self.gender = gender
        self.spells = spells
        self.primary_skills = primary_skills
        self.unknown = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


    def to_dict(self) -> dict:
        dict = {
            "absod_id": self.absod_id,
            "owner": self.owner,
            "type": self.type,
        }

        if self.name is not None:
            dict['name'] = self.name
        if self.experience is not None:
            dict['experience'] = self.experience
        if self.portrait is not None:
            dict['portrait'] = self.portrait
        if self.secondary_skills is not None:
            dict['secondary_skills'] = [ss.to_dict() for ss in self.secondary_skills]
        if self.creatures is not None:
            dict['creatures'] = [creature.to_dict() for creature in self.creatures]

        dict['formation'] = self.formation

        if self.artifacts is not None:
            dict['artifacts'] = self.artifacts.to_dict()

        dict['patrol_radius'] = self.patrol_radius

        if self.biography is not None:
            dict['biography'] = self.biography

        dict['gender'] = self.gender

        if self.spells is not None:
            dict['spells'] = self.spells.to_dict()
        if self.primary_skills is not None:
            dict['primary_skills'] = self.primary_skills.to_dict()

        dict['unknown'] = self.unknown

        return dict