from src.classes.additional_info.LossConditions.Details import Details


class LoseTown(Details):
    @classmethod
    def create_default(cls) -> "LoseTown":
        return cls(
            x=0,
            y=0,
            z=0
        )

    def __init__(self, x: int, y: int, z: int) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.z = z

    def to_dict(self) -> dict:
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z,
        }
