from classes.additional_info.VictoryConditions.Details import Details
from classes.Enums.VictoryConditions import VictoryConditions
from classes.Enums.ArtifactType import ArtifactType, ArtifactNum


class TransportArtifact(Details):
    @classmethod
    def create_default(cls) -> "TransportArtifact":
        return cls(
            artifact_type=0, #ArtifactType
            x=0, # coordy destination
            y=0,
            z=0
        )

    def __init__(self, artifact_type: ArtifactNum, x: int, y: int, z: int) -> None:
        self.artifact_type = artifact_type
        self.x = x
        self.y = y
        self.z = z

    def to_dict(self) -> dict:
        return {
            "artifact_type": self.artifact_type,
            "x": self.x,
            "y": self.y,
            "z": self.z
        }