from src.classes.Objects.Properties.Helpers import Guardians
from src.classes.Objects.PropertiesBase import Properties


class Artifact(Properties):
    @classmethod
    def create_default(cls) -> "Artifact":
        return cls(
            guardians= None
        )

    def __int__(self, guardians: Guardians) -> None:
        self.guardians = guardians

    def to_dict(self) -> dict:
        return {
            "guardians": self.guardians.to_dict(),
        }
