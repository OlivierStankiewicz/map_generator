import sys
import os
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from classes.player.AllowedAlignments import AllowedAlignments

def generate_allowed_alignments() -> AllowedAlignments:
    return AllowedAlignments.create_default()