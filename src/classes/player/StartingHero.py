from classes.player.Heroes import Heroes

class StartingHero(Heroes):

    # no-argument constructor
    @classmethod
    def create_default(cls):
        return cls(
            type= 255, # HEROES
            portrait= 255, #jeśli typ = 255, tego w ogóle nie ma
            name= '' #jeśli typ = 255, tego w ogóle nie ma
        )

    def __init__(self, type: int, portrait: int, name: str) -> None:
        self.portrait = portrait
        super().__init__(type, name)

    def to_dict(self):
        return {
            "type": self.type,
            "portrait": self.portrait,
            "name": self.name
        }