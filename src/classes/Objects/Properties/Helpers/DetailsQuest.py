class Details:
    @classmethod
    def create_default(cls):
        return cls(
            artifacts=[]
        )

    def __init__(self, artifacts: list[int]) -> None:
        self.artifacts= artifacts

    def to_dict(self):
        return {
            "artifacts": self.artifacts
        }