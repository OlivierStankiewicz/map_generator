from classes.Objects.PropertiesBase import Properties

class PlaceholderHero(Properties):

    @classmethod
    def create_default(cls) -> "PlaceholderHero":
        return cls(
            owner= 0,
            type= 255,
            power_rating= 1
        )

    def __init__(self, owner: int,
                        type: int,
                        power_rating: int) -> None:
        self.owner = owner
        self.type = type
        self.power_rating = power_rating

    def to_dict(self) -> dict:
        return {
            "owner": self.owner,
            "type": self.type,
            "power_rating": self.power_rating
        }
