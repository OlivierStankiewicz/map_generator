from classes.player.AllowedAlignments import AllowedAlignments
from classes.player.StartingHero import StartingHero

class Player:
    @classmethod
    def from_default(self):
        self.can_be_human = 0
        self.can_be_computer = 0
        self.behavior = 0
        self.has_customized_alignments= 76
        self.allowed_alignments= AllowedAlignments.from_default()
        self.allow_random_alignment= 0
        self.has_random_heroes= 0
        self.starting_hero= StartingHero.from_default()
        self.num_nonspecific_placeholder_heroes= 0
        self.heroes= []

    def __init__(self, can_be_human: int, can_be_computer: int, behavior: int, has_customized_alignments: int,
                 allowed_alignments: AllowedAlignments, allow_random_alignment: int, has_random_heroes: int,
                 starting_hero: StartingHero, num_nonspecific_placeholder_heroes: int, heroes: list):
        self.can_be_human = can_be_human
        self.can_be_computer = can_be_computer
        self.behavior = behavior
        self.has_customized_alignments = has_customized_alignments
        self.allowed_alignments = allowed_alignments
        self.allow_random_alignment = allow_random_alignment
        self.has_random_heroes = has_random_heroes
        self.starting_hero = starting_hero
        self.num_nonspecific_placeholder_heroes = num_nonspecific_placeholder_heroes
        self.heroes = heroes

    def to_dict(self):
        return {
            "can_be_human": self.can_be_human,
            "can_be_computer": self.can_be_computer,
            "behavior": self.behavior,
            "has_customized_alignments": self.has_customized_alignments,
            "allowed_alignments": self.allowed_alignments.to_dict(),
            "allow_random_alignment": self.allow_random_alignment,
            "has_random_heroes": self.has_random_heroes,
            "starting_hero": self.starting_hero.to_dict(),
            "num_nonspecific_placeholder_heroes": self.num_nonspecific_placeholder_heroes,
            "heroes": [hero for hero in self.heroes]
        }