from Details import Details


class AccumulateResources(Details):
    @classmethod
    def create_default(cls) -> "AccumulateResources":
        return cls(
            allow_normal_win=0,
            applies_to_computer=0,
            resource_type=0, #ResourceType.?
            amount=0
        )

    def __init__(self, allow_normal_win: int, applies_to_computer: int, resource_type: int,
                 amount: int) -> None:
        super().__init__(allow_normal_win, applies_to_computer)
        self.resource_type = resource_type
        self.amount = amount

    def to_dict(self) -> dict:
        dict = super().to_dict()
        dict.update({
            "resource_type": self.resource_type,
            "amount": self.amount
        })
        return dict
