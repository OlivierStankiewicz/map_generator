from classes.Enums.LossConditions import LossConditions
from classes.additional_info.LossConditions.Details import Details

class LossCondition:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "LossCondition":
        return cls(
            type=LossConditions.NORMAL,
        )

    def __init__(self, type: LossConditions) -> None:
        self.type = type
        self.details = Details.create_default()

    def to_dict(self) -> dict:
        _dict = {
            "type": self.type.value
        }
        _dict.update(self.details.to_dict())
        return _dict