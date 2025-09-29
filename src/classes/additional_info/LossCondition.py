from src.classes.Enums.LossConditions import LossConditions
from src.classes.additional_info.LossConditions.Details import Details


class LossCondition:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "LossCondition":
        return cls(
            type=LossConditions.NORMAL
        )

    def __init__(self, type: int) -> None:
        self.type = type
        self.details = Details.get_type(type)

    def to_dict(self) -> dict:
        dict = {
            "type": self.type
        }
        dict.update(self.details.to_dict())
        return dict