class Details:
    @classmethod
    def create_default(cls) -> "Details":
        return cls(
            type= 0,
            amount= 0
        )

    def __init__(self, type: int, amount: int) -> None:
        self.type = type
        self.amount = amount

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "amount": self.amount
        }