from classes.additional_info.VictoryConditions.Details import Details
from classes.Enums.VictoryConditions import VictoryConditions

class FlagMines(Details):

    @classmethod
    def create_default(cls) -> "FlagMines":
        return cls (
            allow_normal_win=0, # def: raczej 1
            applies_to_computer=0 #def: idk
        )

    def __init__(self, allow_normal_win: int, applies_to_computer: int) -> None:
        super().__init__(allow_normal_win, applies_to_computer, VictoryConditions.FLAG_MINES)

    def to_dict(self) -> dict:
        return super().to_dict()