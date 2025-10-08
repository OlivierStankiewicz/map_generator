from classes.player.StartingHero import StartingHero
from classes.player.AllowedAlignments import AllowedAlignments
from classes.player.Heroes import Heroes
from classes.player.MainTown import MainTown
from classes.Enums.Behavior import Behavior

class Player:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "Player":
        return cls(
            can_be_human = 1, # 1 - True, 0 - False, def 1
            can_be_computer = 1, # 1 - True, 0 - False, def 1
            behavior = Behavior.RANDOM.value, #Enums->Behaviors, def Behaviors.RANDOM
            has_customized_alignments= 0, # it can have other values but idk how
            allowed_alignments= AllowedAlignments.create_default(),
            allow_random_alignment= 0, #0?
            main_town = None, # MainTown.create_default(), # default None
            has_random_heroes= 0, #0
            starting_hero= StartingHero.create_default(),
            num_nonspecific_placeholder_heroes= 0, # def: 0 I also saw 1 and 255 but idk
            heroes= []
        )

    def __init__(self, can_be_human: int, can_be_computer: int, behavior: int, has_customized_alignments: int,
                 allowed_alignments: AllowedAlignments, allow_random_alignment: int, main_town: MainTown, has_random_heroes: int,
                 starting_hero: StartingHero, num_nonspecific_placeholder_heroes: int, heroes: list[Heroes]) -> None:
        self.can_be_human = can_be_human
        self.can_be_computer = can_be_computer
        self.behavior = behavior
        self.has_customized_alignments = has_customized_alignments
        self.allowed_alignments = allowed_alignments
        self.allow_random_alignment = allow_random_alignment
        self.main_town = main_town
        self.has_random_heroes = has_random_heroes
        self.starting_hero = starting_hero
        self.num_nonspecific_placeholder_heroes = num_nonspecific_placeholder_heroes
        self.heroes = heroes

    def to_dict(self) -> dict:
        return {
            "can_be_human": self.can_be_human,
            "can_be_computer": self.can_be_computer,
            "behavior": self.behavior,
            "has_customized_alignments": self.has_customized_alignments,
            "allowed_alignments": self.allowed_alignments.to_dict(),
            "allow_random_alignment": self.allow_random_alignment,
            # "main_town": self.main_town.to_dict() if self.main_town else None,
            "has_random_heroes": self.has_random_heroes,
            "starting_hero": self.starting_hero.to_dict(),
            "num_nonspecific_placeholder_heroes": self.num_nonspecific_placeholder_heroes,
            "heroes": [hero.to_dict() for hero in self.heroes]
        }