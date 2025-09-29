from src.classes.additional_info.VictoryConditions.Details import Details


class TransportArtifact(Details):
    @classmethod
    def create_default(cls) -> "TransportArtifact":
        return cls(
            allow_normal_win=0,
            applies_to_computer=0,
            artifact_type=0, #ArtifactType
            x=0, # coordy destination
            y=0,
            z=0
        )

    def __init__(self, allow_normal_win: int, applies_to_computer: int, artifact_type:int, x: int, y: int, z: int) -> None:
        super().__init__(allow_normal_win, applies_to_computer)
        self.artifact_type = artifact_type
        self.x = x
        self.y = y
        self.z = z

    def to_dict(self) -> dict:
        dict = super().to_dict()
        dict.update({
            "artifact_type": self.artifact_type,
            "x": self.x,
            "y": self.y,
            "z": self.z
        })
        return dict
