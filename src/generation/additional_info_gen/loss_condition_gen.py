import sys
import os
from dataclasses import dataclass
# Ensure that imports are done from the level of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from classes.additional_info.LossCondition import LossCondition
from classes.additional_info.LossConditions.LoseTown import LoseTown
from classes.additional_info.LossConditions.LoseHero import LoseHero
from classes.additional_info.LossConditions.TimeExpires import TimeExpires
from classes.additional_info.LossConditions.Details import Details

from classes.Enums.LossConditions import LossConditions

@dataclass
class LossConditionParams:
    loss_condition: LossConditions
    x: int = 255
    y: int = 255
    z: int = 255
    days: int = 0

def generate_loss_condition(loss_condition_params: LossConditionParams) -> LossCondition:
    details: Details = None
    if loss_condition_params is None or loss_condition_params.loss_condition is None or loss_condition_params.loss_condition == LossConditions.NORMAL:
        return LossCondition.create_default()
    elif loss_condition_params.loss_condition == LossConditions.LOSE_TOWN:
        details = LoseTown(loss_condition_params.x, loss_condition_params.y, loss_condition_params.z)
    elif loss_condition_params.loss_condition == LossConditions.LOSE_HERO:
        details = LoseHero(loss_condition_params.x, loss_condition_params.y, loss_condition_params.z)
    elif loss_condition_params.loss_condition == LossConditions.TIME_EXPIRES:
        details = TimeExpires(loss_condition_params.days)

    return LossCondition(
            type=loss_condition_params.loss_condition,
            details=details)