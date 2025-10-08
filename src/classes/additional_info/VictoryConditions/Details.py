
class Details:

    @classmethod
    def create_default(cls) -> "Details":
        return cls (
            allow_normal_win=0, # def: raczej 1
            applies_to_computer=0 #def: idk
        )

    def __init__(self, allow_normal_win: int, applies_to_computer: int) -> None:
        self.allow_normal_win = allow_normal_win
        self.applies_to_computer = applies_to_computer

    def to_dict(self) -> dict:
        return {
            'allow_normal_win': self.allow_normal_win,
            'applies_to_computer': self.applies_to_computer
        }

    # def get_type(self, type: int):
    #     if type == VictoryConditions.NORMAL:
    #         return self.create_default()
    #     elif type == VictoryConditions.ACQUIRE_ARTIFACT:
    #         return AcquireArtifact.create_default()
    #     elif type == VictoryConditions.ACCUMULATE_CREATURES:
    #         return AccumulateCreatures.create_default()
    #     elif type == VictoryConditions.ACCUMULATE_RESOURCES:
    #         return AccumulateResources.create_default()
    #     elif type == VictoryConditions.UPGRADE_TOWN:
    #         return UpgradeTown.create_default()
    #     elif type == VictoryConditions.BUILD_GRAIL:
    #         return BuildGrail.create_default()
    #     elif type == VictoryConditions.DEFEAT_HERO:
    #         return DefeatHero.create_default()
    #     elif type == VictoryConditions.CAPTURE_TOWN:
    #         return CaptureTown.create_default()
    #     elif type == VictoryConditions.DEFEAT_MONSTER:
    #         return DefeatMonster.create_default()
    #     elif type == VictoryConditions.FLAG_DWELLINGS:
    #         return FlagDwellings.create_default()
    #     elif type == VictoryConditions.FLAG_MINES:
    #         return FlagMines.create_default()
    #     elif type == VictoryConditions.TRANSPORT_ARTIFACT:
    #         return TransportArtifact.create_default()
    #     else:
    #         raise Exception(f"Unknown type: {type}")