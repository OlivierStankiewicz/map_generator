import sys
import os
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from classes.additional_info.AdditionalInfo import AdditionalInfo
from generation.additional_info_gen.victory_condition_gen import generate_victory_condition
from generation.additional_info_gen.loss_condition_gen import generate_loss_condition
from generation.additional_info_gen.teams_gen import generate_teams
from generation.additional_info_gen.heroes_availability_gen import generate_heroes_availability
from generation.additional_info_gen.disabled_artifacts_gen import generate_disabled_artifacts
from generation.additional_info_gen.disabled_spells_gen import generate_disabled_spells
from generation.additional_info_gen.disabled_skills_gen import generate_disabled_skills

def generate_additional_info() -> AdditionalInfo:
    return AdditionalInfo(
        victory_condition = generate_victory_condition(),
        loss_condition = generate_loss_condition(),
        teams = generate_teams(),
        heroes_availability = generate_heroes_availability(),
        placeholder_heroes = [],
        custom_heroes = [],
        reserved = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        disabled_artifacts = generate_disabled_artifacts(),
        disabled_spells = generate_disabled_spells(),
        disabled_skills = generate_disabled_skills(),
        rumors = [],
        heroes_settings = []
    )