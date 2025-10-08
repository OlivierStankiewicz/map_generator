from classes.Enums.Behavior import Behavior
from classes.player.AllowedAlignments import AllowedAlignments
from classes.player.StartingHero import StartingHero
from classes.player.Player import Player
from generation.player_gen.allowed_alignments_gen import generate_allowed_alignments
from generation.player_gen.starting_hero_gen import generate_starting_hero

def generate_player() -> Player:
    return Player(
        can_be_human=1,  # 1 - True, 0 - False, def 1
        can_be_computer=1,  # 1 - True, 0 - False, def 1
        behavior=Behavior.RANDOM.value,  # Enums->Behaviors, def Behaviors.RANDOM
        has_customized_alignments=0,  # it can have other values but idk how
        allowed_alignments=AllowedAlignments.create_default(),
        allow_random_alignment=0,  # 0?
        main_town=None,  # MainTown.create_defaults(), def None
        has_random_heroes=0,  # 0
        starting_hero=StartingHero.create_default(),
        num_nonspecific_placeholder_heroes=0,  # def: 0 I also saw 1 and 255 but idk
        heroes=[]
    )