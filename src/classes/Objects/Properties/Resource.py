from classes.Objects.PropertiesBase import Properties

class Resource(Properties):

    @classmethod
    def create_default(cls) -> "Resource":
        return cls(
            quantity= 0
        )

    def __init__(self, quantity: int) -> None:
        self.quantity = quantity
        self.unknown = [0, 0, 0, 0]

    def to_dict(self) -> dict:
        return {
            "quantity": self.quantity,
            "unknown": self.unknown
        }