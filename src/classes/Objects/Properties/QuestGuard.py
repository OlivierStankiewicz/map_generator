from classes.Objects.PropertiesBase import Properties
from classes.Objects.Properties.Helpers.Quest import Quest

class QuestGuard(Properties):

    @classmethod
    def create_default(cls) -> "QuestGuard":
        return cls(
            quest= Quest.create_default()
        )

    def __init__(self, quest: Quest) -> None:
        self.quest = quest

    def to_dict(self) -> dict:
        return {
            "quest": self.quest.to_dict()
        }