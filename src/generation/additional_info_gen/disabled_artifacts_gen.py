import sys
import os
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from classes.additional_info.DisabledArtifacts import DisabledArtifacts

def generate_disabled_artifacts() -> DisabledArtifacts:
    return DisabledArtifacts.create_default()