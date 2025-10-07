from src.classes.Objects.PropertiesBase import Properties



class Grail(Properties):

    @classmethod
    def create_defaults(cls) -> "Grail":
        return cls(
            allowed_radius= 0,
            unknown= [0, 0, 0]
            )

    def __int__(self, allowed_radius: int, unknown: list[int]) -> None:
        self.allowed_radius = allowed_radius
        self.unknown = unknown

    def to_dict(self) -> dict:
        return {
            "allowed_radius": self.allowed_radius,
            "unknown": self.unknown
        }