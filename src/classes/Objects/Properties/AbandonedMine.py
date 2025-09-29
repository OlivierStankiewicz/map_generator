from src.classes.Objects import Properties
from src.classes.Objects.Properties.Helpers.PotentialResources import PotentialResources


class AbandonedMine(Properties):
    @classmethod
    def create_default(cls) -> "AbandonedMine":
        return cls(
            potential_resources= PotentialResources.create_default(),
            unknown= [0, 0, 0]
        )

    def __int__(self, potential_resources: PotentialResources, unknown: list) -> None:
        self.potential_resources = potential_resources
        self.unknown= unknown

    def to_dict(self) -> dict:
        return {
            "potential_resources": self.potential_resources.to_dict(),
            "unknown": self.unknown
        }
