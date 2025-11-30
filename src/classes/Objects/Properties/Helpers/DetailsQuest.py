from classes.Objects.Properties.Helpers.Creatures import Creatures
from classes.Objects.Properties.Helpers.PrimarySkills import PrimarySkills
from classes.Objects.Properties.Helpers.Resources import Resources


class Details:
    @classmethod
    def create_default(cls):
        return cls()

    def __init__(self, level: int = None,
                 skills: PrimarySkills = None, # technicznie po prostu skills
                 absod_id: int = None,
                 artifacts: list[int] = None,
                 creatures: list[Creatures] = None,
                 resources: Resources = None,
                 hero: int = None,
                 player: int = None) -> None:
        self.level = level
        self.skills = skills
        self.absod_id = absod_id
        self.artifacts= artifacts
        self.creatures = creatures
        self.resources = resources
        self.hero = hero
        self.player = player


    def to_dict(self):
        dict = {}
        if self.level is not None:
            dict['level'] = self.level
        elif self.skills is not None:
            dict['skills'] = self.skills.to_dict()
        elif self.absod_id is not None:
            dict['absod_id'] = self.absod_id
        elif self.artifacts is not None:
            dict['artifacts'] = self.artifacts
        elif self.creatures is not None:
            dict['creatures'] = [creature.to_dict() for creature in self.creatures]
        elif self.resources is not None:
            dict['resources'] = self.resources.to_dict()
        elif self.hero is not None:
            dict['hero'] = self.hero
        elif self.player is not None:
            dict['player'] = self.player
        return dict
