import sys
import os
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.ObjectsTemplate import ObjectsTemplate

def generate_objects_template() -> ObjectsTemplate:
    return ObjectsTemplate.create_default()