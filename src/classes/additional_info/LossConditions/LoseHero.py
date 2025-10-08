from typing import TYPE_CHECKING
from classes.Enums.LossConditions import LossConditions

if TYPE_CHECKING:
    from classes.additional_info.LossConditions.LoseHero import LoseHero
    from classes.additional_info.LossConditions.LoseTown import LoseTown
    from classes.additional_info.LossConditions.TimeExpires import TimeExpires

class Details:

    @classmethod
    def create_default(cls) -> "Details":
        return cls()

    def __init__(self) -> None:
        return

    def to_dict(self) -> dict:
        return {}

    @classmethod
    def get_type(self, type: int):
        if type == LossConditions.NORMAL:
            return self.create_default()
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