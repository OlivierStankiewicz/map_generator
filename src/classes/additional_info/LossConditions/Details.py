from typing import TYPE_CHECKING
from classes.Enums.LossConditions import LossConditions

if TYPE_CHECKING:
    from classes.additional_info.LossConditions.LoseHero import LoseHero
    from classes.additional_info.LossConditions.LoseTown import LoseTown
    from classes.additional_info.LossConditions.TimeExpires import TimeExpires

class Details:

    @classmethod
    def create_default(cls) -> "Details":
        return cls(
            loseCondition_type=LossConditions.NORMAL
        )

    def __init__(self, loseCondition_type: LossConditions) -> None:
        self.loseCondition_type = loseCondition_type

    def to_dict(self) -> dict:
        dict = {}
        if self.loseCondition_type != LossConditions.NORMAL:
            dict['loseCondition_type'] = self.get_type(self.loseCondition_type).to_dict()
        return dict

    @classmethod
    def get_type(cls, type: LossConditions):
        if type == LossConditions.NORMAL:
            return cls.create_default()
        elif type == LossConditions.LOSE_TOWN:
            return LoseTown.create_default()
        elif type == LossConditions.LOSE_HERO:
            # Lazy import inside the method
            from classes.additional_info.LossConditions.LoseHero import LoseHero
            return LoseHero.create_default()
        elif type == LossConditions.TIME_EXPIRES:
            return TimeExpires.create_default()
        else:
            raise Exception(f"Unknown type: {type}")