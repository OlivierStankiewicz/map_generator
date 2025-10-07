from src.classes.Objects.PropertiesBase import Properties


class Resource(Properties):

    @classmethod
    def create_default(cls) -> "Resource":
        return cls(
            quantity= 0,
            unknown = []
        )

    def __init__(self, quantity: int, unknown: list[int]) -> None:
        self.quantity = quantity
        self.unknown = unknown

    def to_dict(self) -> dict:
        return {
            "quantity": self.quantity,
            "unknown": self.unknown
        }