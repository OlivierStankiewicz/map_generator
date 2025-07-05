import sys
import os
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from classes.player.Player import Player
from generation.player_gen.allowed_alignments_gen import generate_allowed_alignments
from generation.player_gen.starting_hero_gen import generate_starting_hero

def generate_player() -> Player:
    return Player(
        can_be_human = 0,
        can_be_computer = 0,
        behavior = 0,
        has_customized_alignments= 76,
        allowed_alignments= generate_allowed_alignments(),
        allow_random_alignment= 0,
        has_random_heroes= 0,
        starting_hero= generate_starting_hero(),
        num_nonspecific_placeholder_heroes= 0,
        heroes= []
    )