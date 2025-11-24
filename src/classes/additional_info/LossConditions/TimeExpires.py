from classes.additional_info.LossConditions.Details import Details
from classes.Enums.LossConditions import LossConditions

class TimeExpires(Details):
    @classmethod
    def create_default(cls) -> "TimeExpires":
        return cls(
            days= 0
        )

    def __init__(self, days: int) -> None:
        self.days = days

    def to_dict(self) -> dict:
        return {
            'days': self.days
        }

# 1 tydzie� = 7 dni
# 1 miesi�c = 4 tygodnie = 28 dni
# 1 rok = 12 miesi�cy = 48 tygodni = 336 dni