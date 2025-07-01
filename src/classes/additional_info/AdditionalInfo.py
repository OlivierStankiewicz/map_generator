from classes.additional_info.VictoryCondition import VictoryCondition
from classes.additional_info.LossCondition import LossCondition
from classes.additional_info.Teams import Teams
from classes.additional_info.HeroesAvailability import HeroesAvailability
from classes.additional_info.DisabledArtifacts import DisabledArtifacts
from classes.additional_info.DisabledSpells import DisabledSpells
from classes.additional_info.DisabledSkills import DisabledSkills

class AdditionalInfo:
    @classmethod
    def from_default(self):
        self.victory_condition = VictoryCondition.from_default()
        self.loss_condition = LossCondition.from_default()
        self.teams = Teams.from_default()
        self.heroes_availability = HeroesAvailability.from_default()
        self.placeholder_heroes = []
        self.custom_heroes = []
        self.reserved = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.disabled_artifacts = DisabledArtifacts.from_default()
        self.disabled_spells = DisabledSpells.from_default()
        self.disabled_skills = DisabledSkills.from_default()
        self.rumors = []
        self.heroes_settings = []

    def __init__(self, victory_condition: VictoryCondition, loss_condition: LossCondition, teams: Teams,
                 heroes_availability: HeroesAvailability, placeholder_heroes: list, custom_heroes: list,
                 reserved: list[int], disabled_artifacts: DisabledArtifacts, disabled_spells: DisabledSpells,
                 disabled_skills: DisabledSkills, rumors: list, heroes_settings: list):
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

    def to_dict(self):
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
            "rumors": self.rumors,
            "heroes_settings": self.heroes_settings
        }