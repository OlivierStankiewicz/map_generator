from classes.additional_info.VictoryConditions.Details import Details
from classes.Enums.VictoryConditions import VictoryConditions
from classes.Enums.CreatureType import CreatureType, CreatureNum


class AccumulateCreatures(Details):
    @classmethod
    def create_default(cls) -> "AccumulateCreatures":
        return cls(
            allow_normal_win=0,
            applies_to_computer=0,
            creature_type=0, #CreatureType.?
            count=0
        )

    def __init__(self, allow_normal_win: int, applies_to_computer: int, creature_type: CreatureNum,
                 count: int) -> None:
        super().__init__(allow_normal_win, applies_to_computer, VictoryConditions.ACCUMULATE_CREATURES)
        self.creature_type = creature_type
        self.count = count

    def to_dict(self) -> dict:
        _dict = super().to_dict()
        _dict.update({
            "creature_type": self.creature_type.value,
            "count": self.count
        })
        return _dict

