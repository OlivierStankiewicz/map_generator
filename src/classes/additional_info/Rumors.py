

class Rumors:
    @classmethod
    def create_default(cls) -> "Rumors":
        return cls(
            name="",
            description=""
        )

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description
        }
