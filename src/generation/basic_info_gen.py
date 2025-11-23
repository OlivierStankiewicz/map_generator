import sys
import os
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.BasicInfo import BasicInfo

def generate_default_basic_info() -> BasicInfo:
    return BasicInfo.create_default()

def generate_basic_info(is_playable: int = 1, map_size: int = 72, has_two_levels: int = 1,
                 name: str = "", description: str = "", difficulty: int = 1, max_hero_level: int = 0) -> BasicInfo:
    return BasicInfo(
        is_playable= is_playable,
        map_size= map_size,
        has_two_levels= has_two_levels,
        name= name,
        description= description,
        difficulty= difficulty,
        max_hero_level= max_hero_level
    )