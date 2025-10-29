import sys
import os
from dataclasses import dataclass
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from classes.additional_info.VictoryCondition import VictoryCondition
from classes.additional_info.VictoryConditions.AccumulateCreatures import AccumulateCreatures
from classes.additional_info.VictoryConditions.AccumulateResources import AccumulateResources
from classes.additional_info.VictoryConditions.AcquireArtifact import AcquireArtifact
from classes.additional_info.VictoryConditions.BuildGrail import BuildGrail
from classes.additional_info.VictoryConditions.CaptureTown import CaptureTown
from classes.additional_info.VictoryConditions.DefeatHero import DefeatHero
from classes.additional_info.VictoryConditions.DefeatMonster import DefeatMonster
from classes.additional_info.VictoryConditions.Details import Details
from classes.additional_info.VictoryConditions.FlagDwellings import FlagDwellings
from classes.additional_info.VictoryConditions.FlagMines import FlagMines
from classes.additional_info.VictoryConditions.TransportArtifact import TransportArtifact
from classes.additional_info.VictoryConditions.UpgradeTown import UpgradeTown

from classes.Enums.VictoryConditions import VictoryConditions
from classes.Enums.ArtifactType import ArtifactType
from classes.Enums.CreatureType import CreatureType
from classes.Enums.ResourceType import ResourceType
from classes.Enums.HallLevel import HallLevel
from classes.Enums.CastleLevel import CastleLevel

@dataclass
class VictoryConditionParams():
    victory_condition: VictoryConditions
    allow_normal_win: int
    applies_to_computer: int
    # ACQUIRE_ARTIFACT | TRANSPORT_ARTIFACT
    artifact_type: ArtifactType = None
    # ACCUMULATE CREATURES
    creature_type: CreatureType = None
    count: int = 0
    # ACCUMULATE RESOURCES
    resource_type: ResourceType = None
    amount: int = 0
    # UPGRADE_TOWN | BUILD_GRAIL | DEFEAT_HERO | CAPTURE_TOWN | DEFEAT_MONSTER | TRANSPORT_ARTIFACT
    x: int = 255
    y: int = 255
    z: int = 255
    # UPGRADE_TOWN
    hall_level: HallLevel = None
    castle_level: CastleLevel = None

def generate_victory_condition(victory_condition_params: VictoryConditionParams) -> VictoryCondition:
    details: Details = None
    if victory_condition_params is None or victory_condition_params.victory_condition is None or victory_condition_params.victory_condition == VictoryConditions.NORMAL:
        return VictoryCondition.create_default()
    elif victory_condition_params.victory_condition == VictoryConditions.ACQUIRE_ARTIFACT:
        details = AcquireArtifact(victory_condition_params.allow_normal_win, victory_condition_params.applies_to_computer, victory_condition_params.artifact_type)
    elif victory_condition_params.victory_condition == VictoryConditions.ACCUMULATE_CREATURES:
        details = AccumulateCreatures(victory_condition_params.allow_normal_win, victory_condition_params.applies_to_computer, victory_condition_params.creature_type, victory_condition_params.count)
    elif victory_condition_params.victory_condition == VictoryConditions.ACCUMULATE_RESOURCES:
        details = AccumulateResources(victory_condition_params.allow_normal_win, victory_condition_params.applies_to_computer, victory_condition_params.resource_type, victory_condition_params.amount)
    elif victory_condition_params.victory_condition == VictoryConditions.UPGRADE_TOWN:
        details = UpgradeTown(victory_condition_params.allow_normal_win, victory_condition_params.applies_to_computer, victory_condition_params.x, victory_condition_params.y, victory_condition_params.z, victory_condition_params.hall_level, victory_condition_params.castle_level)
    elif victory_condition_params.victory_condition == VictoryConditions.BUILD_GRAIL:
        details = BuildGrail(victory_condition_params.allow_normal_win, victory_condition_params.applies_to_computer, victory_condition_params.x, victory_condition_params.y, victory_condition_params.z)
    elif victory_condition_params.victory_condition == VictoryConditions.DEFEAT_HERO:
        details = DefeatHero(victory_condition_params.allow_normal_win, victory_condition_params.applies_to_computer, victory_condition_params.x, victory_condition_params.y, victory_condition_params.z)
    elif victory_condition_params.victory_condition == VictoryConditions.CAPTURE_TOWN:
        details = CaptureTown(victory_condition_params.allow_normal_win, victory_condition_params.applies_to_computer, victory_condition_params.x, victory_condition_params.y, victory_condition_params.z)
    elif victory_condition_params.victory_condition == VictoryConditions.DEFEAT_MONSTER:
        details = DefeatMonster(victory_condition_params.allow_normal_win, victory_condition_params.applies_to_computer, victory_condition_params.x, victory_condition_params.y, victory_condition_params.z)
    elif victory_condition_params.victory_condition == VictoryConditions.FLAG_DWELLINGS:
        details = FlagDwellings(victory_condition_params.allow_normal_win, victory_condition_params.applies_to_computer)
    elif victory_condition_params.victory_condition == VictoryConditions.FLAG_MINES:
        details = FlagMines(victory_condition_params.allow_normal_win, victory_condition_params.applies_to_computer)
    elif victory_condition_params.victory_condition == VictoryConditions.TRANSPORT_ARTIFACT:
        details = TransportArtifact(victory_condition_params.allow_normal_win, victory_condition_params.applies_to_computer, victory_condition_params.artifact_type, victory_condition_params.x, victory_condition_params.y, victory_condition_params.z)

    return VictoryCondition(
            type=victory_condition_params.victory_condition,
            details=details)