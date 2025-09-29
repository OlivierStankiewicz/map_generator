class Creatures:
    @classmethod
    def create_default(cls) -> "Creatures":
        return cls(
            type= 65535, #None
            count= 0
        )

    def __init__(self, type: int, count: int) -> None:
        self.type = type
        self.count = count

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "count": self.count
        }