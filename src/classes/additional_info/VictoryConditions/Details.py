from typing import TYPE_CHECKING
from classes.Enums.VictoryConditions import VictoryConditions


class Details:

    @classmethod
    def create_default(cls) -> "Details":
        return cls (
        )

    def __init__(self) -> None:
        pass

    def to_dict(self):
        return {}

