from src.classes.Objects import Properties
from src.classes.Objects.Properties.Helpers.Quest import Quest
from src.classes.Objects.Properties.Helpers.Reward import Reward


class SeersHut(Properties):
    @classmethod
    def create_default(cls) -> "SeersHut":
        return cls(
            quest=Quest.create_default(),
            reward= Reward.create_default(),
            unknown=[]
        )

    def __init__(self, quest: Quest, reward: Reward, unknown: list[int]) -> None:
        self.quest = quest
        self.reward = reward
        self.unknown = unknown

    def to_dict(self) -> dict:
        return {
            "quest": self.quest.to_dict(),
            "reward": self.reward.to_dict(),
            "unknown": self.unknown
        }