import sys
import os
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from classes.tile.Flags import Flags

def generate_flags() -> Flags:
    return Flags.create_default()