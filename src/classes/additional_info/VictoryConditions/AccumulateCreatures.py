from classes.additional_info.VictoryConditions.Details import Details
from classes.Enums.VictoryConditions import VictoryConditions
from classes.Enums.CreatureType import CreatureType, CreatureNum


class AccumulateCreatures(Details):
    @classmethod
    def create_default(cls) -> "AccumulateCreatures":
        return cls(
            creature_type=0, #CreatureType.?
            count=0
        )

    def __init__(self, creature_type: CreatureNum,
                 count: int) -> None:
        self.creature_type = creature_type
        self.count = count

    def to_dict(self) -> dict:
        return {
            "creature_type": self.creature_type,
            "count": self.count
        }

