from typing import TYPE_CHECKING
from classes.Enums.VictoryConditions import VictoryConditions

if TYPE_CHECKING:
    from classes.additional_info.VictoryConditions.AcquireArtifact import AcquireArtifact
    from classes.additional_info.VictoryConditions.AccumulateCreatures import AccumulateCreatures
    from classes.additional_info.VictoryConditions.AccumulateResources import AccumulateResources
    from classes.additional_info.VictoryConditions.UpgradeTown import UpgradeTown
    from classes.additional_info.VictoryConditions.BuildGrail import BuildGrail
    from classes.additional_info.VictoryConditions.DefeatHero import DefeatHero
    from classes.additional_info.VictoryConditions.CaptureTown import CaptureTown
    from classes.additional_info.VictoryConditions.DefeatMonster import DefeatMonster
    from classes.additional_info.VictoryConditions.FlagDwellings import FlagDwellings
    from classes.additional_info.VictoryConditions.FlagMines import FlagMines
    from classes.additional_info.VictoryConditions.TransportArtifact import TransportArtifact

class Details:

    @classmethod
    def create_default(cls) -> "Details":
        return cls (
            allow_normal_win=0, # def: raczej 1
            applies_to_computer=0, #def: idk
            victory_condition_type=VictoryConditions.NORMAL
        )

    def __init__(self, allow_normal_win: int, applies_to_computer: int, victory_condition_type: VictoryConditions) -> None:
        self.allow_normal_win = allow_normal_win
        self.applies_to_computer = applies_to_computer
        self.victory_condition_type = victory_condition_type

    def to_dict(self) -> dict:
        dict =  {
            'allow_normal_win': self.allow_normal_win,
            'applies_to_computer': self.applies_to_computer,
        }
        if self.victory_condition_type != VictoryConditions.NORMAL:
            dict['victory_condition_type'] = self.get_type(self.victory_condition_type).to_dict()
        return dict

    @classmethod
    def get_type(cls, type: VictoryConditions):
        if type == VictoryConditions.NORMAL:
            return cls.create_default()
        elif type == VictoryConditions.ACQUIRE_ARTIFACT:
            # Lazy import inside the method
            from classes.additional_info.VictoryConditions.AcquireArtifact import AcquireArtifact
            return AcquireArtifact.create_default()
        elif type == VictoryConditions.ACCUMULATE_CREATURES:
            # Lazy import inside the method
            from classes.additional_info.VictoryConditions.AccumulateCreatures import AccumulateCreatures
            return AccumulateCreatures.create_default()
        elif type == VictoryConditions.ACCUMULATE_RESOURCES:
            # Lazy import inside the method
            from classes.additional_info.VictoryConditions.AccumulateResources import AccumulateResources
            return AccumulateResources.create_default()
        elif type == VictoryConditions.UPGRADE_TOWN:
            # Lazy import inside the method
            from classes.additional_info.VictoryConditions.UpgradeTown import UpgradeTown
            return UpgradeTown.create_default()
        elif type == VictoryConditions.BUILD_GRAIL:
            # Lazy import inside the method
            from classes.additional_info.VictoryConditions.BuildGrail import BuildGrail
            return BuildGrail.create_default()
        elif type == VictoryConditions.DEFEAT_HERO:
            # Lazy import inside the method
            from classes.additional_info.VictoryConditions.DefeatHero import DefeatHero
            return DefeatHero.create_default()
        elif type == VictoryConditions.CAPTURE_TOWN:
            # Lazy import inside the method
            from classes.additional_info.VictoryConditions.CaptureTown import CaptureTown
            return CaptureTown.create_default()
        elif type == VictoryConditions.DEFEAT_MONSTER:
            # Lazy import inside the method
            from classes.additional_info.VictoryConditions.DefeatMonster import DefeatMonster
            return DefeatMonster.create_default()
        elif type == VictoryConditions.FLAG_DWELLINGS:
            # Lazy import inside the method
            from classes.additional_info.VictoryConditions.FlagDwellings import FlagDwellings
            return FlagDwellings.create_default()
        elif type == VictoryConditions.FLAG_MINES:
            # Lazy import inside the method
            from classes.additional_info.VictoryConditions.FlagMines import FlagMines
            return FlagMines.create_default()
        elif type == VictoryConditions.TRANSPORT_ARTIFACT:
            # Lazy import inside the method
            from classes.additional_info.VictoryConditions.TransportArtifact import TransportArtifact
            return TransportArtifact.create_default()
        else:
            raise Exception(f"Unknown type: {type}")