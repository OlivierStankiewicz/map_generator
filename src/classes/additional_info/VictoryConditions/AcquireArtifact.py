from classes.additional_info.VictoryConditions.Details import Details

class AcquireArtifact(Details):
    @classmethod
    def create_default(cls) -> "AcquireArtifact":
        return cls(
            allow_normal_win=0,
            applies_to_computer=0,
            artifact_type=0 #ArtifactTpe.?
        )

    def __init__(self, allow_normal_win: int, applies_to_computer: int, artifact_type: int) -> None:
        super().__init__(allow_normal_win, applies_to_computer)
        self.artifact_type = artifact_type

    def to_dict(self) -> dict:
        dict = super().to_dict()
        dict.update({
            "artifact_type": self.artifact_type
        })
        return dict
