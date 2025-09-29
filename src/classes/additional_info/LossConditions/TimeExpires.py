from src.classes.additional_info.LossConditions.Details import Details


class TimeExpires(Details):
    @classmethod
    def create_default(cls) -> "TimeExpires":
        return cls(
            days= 0
        )

    def __init__(self, days: int) -> None:
        super().__init__()
        self.days = days

    def to_dict(self) -> dict:
        return {
            'days': self.days
        }

# 1 tydzień = 7 dni
# 1 miesiąc = 4 tygodnie = 28 dni
# 1 rok = 12 miesięcy = 48 tygodni = 336 dni