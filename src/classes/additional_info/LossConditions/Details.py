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
        pass

    def to_dict(self) -> dict:
        return {}