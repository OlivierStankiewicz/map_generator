import sys
import os
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from classes.additional_info.Teams import Teams

def generate_teams() -> Teams:
    return Teams.create_default()