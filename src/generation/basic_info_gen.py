import sys
import os
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.BasicInfo import BasicInfo

def generate_basic_info(map_size=72,
                        name="Generated map",
                        description="This map has been generated",
                        difficulty=1) -> BasicInfo:
    info = BasicInfo.create_default()
    info.map_size = map_size
    info.name = name
    info.description = description
    info.difficulty = difficulty
    return info