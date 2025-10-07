from src.classes.Objects.PropertiesBase import Properties
from src.classes.Objects.Properties.Helpers.AffectedPlayers import AffectedPlayers
from src.classes.Objects.Properties.Helpers.Creatures import Creatures
from src.classes.Objects.Properties.Helpers.PrimarySkills import PrimarySkills
from src.classes.Objects.Properties.Helpers.Resources import Resources
from src.classes.Objects.Properties.Helpers.SecondarySkills import SecondarySkills
from src.classes.Objects.Properties.Helpers.Spells import Spells


class Event(Properties):
    @classmethod
    def create_default(cls) -> "Event":
        return cls(
            experience = 0,
            spell_points = 0, # + ileś lub na - jeśli ma zabierać
            morale = 0, #od -3 do +3
            luck = 0,  #od -3 do +3
            resources = Resources.create_default(),
            primary_skills =  PrimarySkills.create_default(),
            secondary_skills = [],
            artifacts = [],
            spells = [],
            creatures = [], # [Creatures.create_default() for _ in range(7)]
            unknown = [0, 0, 0, 0, 0, 0, 0, 0],
            affected_players = AffectedPlayers.create_default(),
            applies_to_computer = 0,
            remove_after_first_visit = 1,
            unknown2 = [0, 0, 0, 0]
        )

    def __int__(self, experience: int, spell_points: int, morale: int, luck: int, resources: Resources,
                primary_skills: PrimarySkills, secondary_skills: list[SecondarySkills], artifacts: list[int], spells: list[int],
                creatures: list[Creatures], unknown: list[int], affected_players: AffectedPlayers,
                applies_to_computer: int, remove_after_first_visit: int, unknown2: list[int]) -> None:
        self.experience = experience
        self.spell_points = spell_points
        self.morale = morale
        self.luck = luck
        self.resources = resources
        self.primary_skills = primary_skills
        self.secondary_skills = secondary_skills
        self.artifacts = artifacts
        self.spells = spells
        self.creatures = creatures
        self.unknown = unknown
        self.affected_players = affected_players
        self.applies_to_computer = applies_to_computer
        self.remove_after_first_visit = remove_after_first_visit
        self.unknown2 = unknown2

    def to_dict(self) -> dict:
        return {
            'experience': self.experience,
            'spell_points': self.spell_points,
            'morale': self.morale,
            'luck': self.luck,
            'resources': self.resources.to_dict(),
            'primary_skills': self.primary_skills.to_dict(),
            'secondary_skills': [secondary_skill.to_dict() for secondary_skill in self.secondary_skills],
            'artifacts': self.artifacts,
            'spells': [spell for spell in self.spells],
            'creatures': [creature for creature in self.creatures],
            'unknown': self.unknown,
            'affected_players': self.affected_players.to_dict(),
            'applies_to_computer': self.applies_to_computer,
            'remove_after_first_visit': self.remove_after_first_visit,
            'unknown2': self.unknown2
        }
