from classes.Enums.Disposition import Disposition
from classes.Objects.PropertiesBase import Properties
from classes.Objects.Properties.Helpers.MessageAndTreasures import MessageAndTreasures

class Monster(Properties):

    @classmethod
    def create_defaults(cls) -> "Monster":
        return cls(
            absod_id=0,
            count=0,
            disposition=2, #Dispostion enum
            message_and_treasure= MessageAndTreasures.create_default(),
            never_flees=0,
            does_not_grow=0
        )

    def __init__(self, absod_id: int, count: int, disposition: Disposition, message_and_treasure: MessageAndTreasures, never_flees: int,
                does_not_grow: int) -> None:
        self.absod_id = absod_id
        self.count = count
        self.disposition = disposition
        self.message_and_treasure = message_and_treasure
        self.never_flees = never_flees
        self.does_not_grow = does_not_grow
        self.unknown = [0, 0]

    def to_dict(self) -> dict:
        dict = {
            "absod_id": self.absod_id,
            "count": self.count,
            "disposition": self.disposition.value,
            "never_flees": self.never_flees,
            "does_not_grow": self.does_not_grow,
            "unknown": self.unknown
        }
        if self.message_and_treasure is not None:
            dict["message_and_treasure"] = self.message_and_treasure.to_dict()
        return dict
