from classes.additional_info.VictoryCondition import VictoryCondition
from classes.additional_info.LossCondition import LossCondition
from classes.additional_info.Teams import Teams
from classes.additional_info.HeroesAvailability import HeroesAvailability
from classes.additional_info.DisabledArtifacts import DisabledArtifacts
from classes.additional_info.DisabledSpells import DisabledSpells
from classes.additional_info.DisabledSkills import DisabledSkills
from classes.additional_info.Rumors import Rumors

class AdditionalInfo:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "AdditionalInfo":
        return cls(
            victory_condition = VictoryCondition.create_default(),
            loss_condition = LossCondition.create_default(),
            teams = Teams.create_default(),
            heroes_availability = HeroesAvailability.create_default(),
            placeholder_heroes = [],
            custom_heroes = [],
            reserved = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            disabled_artifacts = DisabledArtifacts.create_default(),
            disabled_spells = DisabledSpells.create_default(),
            disabled_skills = DisabledSkills.create_default(),
            rumors = list[Rumors.create_default()],
            heroes_settings = [] #?
        )

    def __init__(self, victory_condition: VictoryCondition, loss_condition: LossCondition, teams: Teams,
                 heroes_availability: HeroesAvailability, placeholder_heroes: list[int], custom_heroes: list,
                 reserved: list[int], disabled_artifacts: DisabledArtifacts, disabled_spells: DisabledSpells,
                 disabled_skills: DisabledSkills, rumors: list[Rumors], heroes_settings: list) -> None:
        self.victory_condition = victory_condition
        self.loss_condition = loss_condition
        self.teams = teams
        self.heroes_availability = heroes_availability
        self.placeholder_heroes = placeholder_heroes
        self.custom_heroes = custom_heroes
        self.reserved = reserved
        self.disabled_artifacts = disabled_artifacts
        self.disabled_spells = disabled_spells
        self.disabled_skills = disabled_skills
        self.rumors = rumors
        self.heroes_settings = heroes_settings

    def to_dict(self) -> dict:
        return {
            "victory_condition": self.victory_condition.to_dict(),
            "loss_condition": self.loss_condition.to_dict(),
            "teams": self.teams.to_dict(),
            "heroes_availability": self.heroes_availability.to_dict(),
            "placeholder_heroes": self.placeholder_heroes,
            "custom_heroes": self.custom_heroes,
            "reserved": self.reserved,
            "disabled_artifacts": self.disabled_artifacts.to_dict(),
            "disabled_spells": self.disabled_spells.to_dict(),
            "disabled_skills": self.disabled_skills.to_dict(),
            "rumors": [rumors.to_dict() for rumors in self.rumors],
            "heroes_settings": self.heroes_settings
        }