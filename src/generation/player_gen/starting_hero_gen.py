import sys
import os
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from classes.player.StartingHero import StartingHero

def generate_starting_hero() -> StartingHero:
    return StartingHero.create_default()