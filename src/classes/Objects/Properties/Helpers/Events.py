from classes.Objects import Properties
from classes.Objects.Properties.Helpers.AffectedPlayers import AffectedPlayers
from classes.Objects.Properties.Helpers.BuildingsEvent import Buildings
from classes.Objects.Properties.Helpers.Creatures import Creatures
from classes.Objects.Properties.Helpers.PrimarySkills import PrimarySkills
from classes.Objects.Properties.Helpers.Resources import Resources
from classes.Objects.Properties.Helpers.SecondarySkills import SecondarySkills
from classes.Objects.Properties.Helpers.Spells import Spells


class Events:
    @classmethod
    def create_default(cls) -> "Events":
        return cls(
            name = '',
            message = '',
            resources = Resources.create_default(),
            affected_players = AffectedPlayers.create_default(),
            applies_to_human = 1,
            applies_to_computer = 1,
            day_of_first_occurence = 0,
            repeat_after_days = 0,
            unknown = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            buildings = Buildings.create_default(),
            creatures = [],
            unknown2 = [0, 0, 0, 0],
        )

    def __int__(self, name: str, message: str, resources: Resources, affected_players: AffectedPlayers,
                applies_to_human: int, applies_to_computer: int, day_of_first_occurence: int, repeat_after_days: int,
                unknown: list[int], buildings: Buildings, creatures: list[int], unknown2: [int]) -> None:
        self.name = name
        self.message = message
        self.resources = resources
        self.affected_players = affected_players
        self.applies_to_human = applies_to_human
        self.applies_to_computer = applies_to_computer
        self.day_of_first_occurence = day_of_first_occurence
        self.repeat_after_days = repeat_after_days
        self.unknown = unknown
        self.buildings = buildings
        self.creatures = creatures
        self.unknown2 = unknown2

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'message': self.message,
            'resources': self.resources.to_dict(),
            'affected_players': self.affected_players.to_dict(),
            'applies_to_human': self.applies_to_human,
            'applies_to_computer': self.applies_to_computer,
            'day_of_first_occurence': self.day_of_first_occurence,
            'repeat_after_days': self.repeat_after_days,
            'unknown': self.unknown,
            'buildings': self.buildings.to_dict(),
            'creatures': self.creatures,
            'unknown2': self.unknown2,
        }
