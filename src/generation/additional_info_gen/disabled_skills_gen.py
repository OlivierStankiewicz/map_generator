import sys
import os
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from classes.additional_info.DisabledSkills import DisabledSkills

def generate_disabled_skills() -> DisabledSkills:
    return DisabledSkills.create_default()