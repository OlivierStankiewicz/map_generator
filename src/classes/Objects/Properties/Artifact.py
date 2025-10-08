from classes.Objects.Properties.Helpers.Guardians import Guardians
from classes.Objects.PropertiesBase import Properties


class Artifact(Properties):
    @classmethod
    def create_default(cls) -> "Artifact":
        return cls(
            guardians=Guardians.create_default()
        )

    def __init__(self, guardians: Guardians) -> None:
        self.guardians = guardians

    def to_dict(self) -> dict:
        return {
            "guardians": self.guardians.to_dict(),
        }
