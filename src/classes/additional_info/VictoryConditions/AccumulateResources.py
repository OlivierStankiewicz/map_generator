from classes.additional_info.VictoryConditions.Details import Details
from classes.Enums.VictoryConditions import VictoryConditions
from classes.Enums.ResourceType import ResourceType


class AccumulateResources(Details):
    @classmethod
    def create_default(cls) -> "AccumulateResources":
        return cls(
            resource_type=ResourceType.WOOD,
            amount=0
        )

    def __init__(self, resource_type: ResourceType,
                 amount: int) -> None:
        self.resource_type = resource_type
        self.amount = amount

    def to_dict(self) -> dict:
        return {
            "resource_type": self.resource_type.value,
            "amount": self.amount
        }
