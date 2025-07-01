class StartingHero:

    # alternative no-argument constructor
    @classmethod
    def create_default(cls):
        return cls(
            type=255
        )

    def __init__(self, type: int):
        self.type = type

    def to_dict(self):
        return {
            "type": self.type
        }