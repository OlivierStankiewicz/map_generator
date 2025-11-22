class Heroes:

    # no-argument constructor
    @classmethod
    def create_default(cls):
        return cls(
            type=255, # Heroes type
            name= ''
        )

    def __init__(self, type: int, name: str) -> None:
        self.type = type
        self.name = name

    def to_dict(self):
        return {
            "type": self.type,
            "name": self.name
        }