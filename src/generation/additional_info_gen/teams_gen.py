import sys
import os
from dataclasses import dataclass

# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from classes.additional_info.Teams import Teams

@dataclass
class TeamsParams:
    num_teams: int
    team_for_player: list = None

def generate_teams(teams_params: TeamsParams) -> Teams:
    return Teams.create_default() if teams_params is None or teams_params.num_teams == 0 else Teams(num_teams=teams_params.num_teams, team_for_player=teams_params.team_for_player)