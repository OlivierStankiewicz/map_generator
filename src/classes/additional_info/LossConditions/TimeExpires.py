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
        super().__init__(LossConditions.TIME_EXPIRES)

    def to_dict(self) -> dict:
        return {
            'days': self.days
        }

# 1 tydzieñ = 7 dni
# 1 miesi¹c = 4 tygodnie = 28 dni
# 1 rok = 12 miesiêcy = 48 tygodni = 336 dni