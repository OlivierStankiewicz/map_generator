from classes.additional_info.VictoryConditions.Details import Details
from classes.Enums.VictoryConditions import VictoryConditions
from classes.Enums.ArtifactType import ArtifactType, ArtifactNum


class AcquireArtifact(Details):
    @classmethod
    def create_default(cls) -> "AcquireArtifact":
        return cls(
            artifact_type=0 #ArtifactTpe.?
        )

    def __init__(self, artifact_type: ArtifactNum) -> None:
        self.artifact_type = artifact_type

    def to_dict(self) -> dict:
        return {
            "artifact_type": self.artifact_type
        }
