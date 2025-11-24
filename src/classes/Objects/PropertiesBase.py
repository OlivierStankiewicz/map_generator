from typing import TYPE_CHECKING
from classes.Enums.ObjectPropertiesType import ObjectPropertiesType

if TYPE_CHECKING:
    from classes.Objects.Properties.AbandonedMine import AbandonedMine
    from classes.Objects.Properties.Artifact import Artifact
    from classes.Objects.Properties.Event import Event
    from classes.Objects.Properties.Garrison import Garrison
    from classes.Objects.Properties.Grail import Grail
    from classes.Objects.Properties.Hero import Hero
    from classes.Objects.Properties.Monster import Monster
    from classes.Objects.Properties.PandorasBox import PandorasBox
    from classes.Objects.Properties.PlaceholderHero import PlaceholderHero
    from classes.Objects.Properties.QuestGuard import QuestGuard
    from classes.Objects.Properties.RandomDwelling import RandomDwelling
    from classes.Objects.Properties.RandomDwellingPresetAlignment import RandomDwellingPresetAlignment
    from classes.Objects.Properties.RandomDwellingPresetLevel import RandomDwellingPresetLevel
    from classes.Objects.Properties.Resource import Resource
    from classes.Objects.Properties.Scholar import Scholar
    from classes.Objects.Properties.SeersHut import SeersHut
    from classes.Objects.Properties.Shrine import Shrine
    from classes.Objects.Properties.Sign import Sign
    from classes.Objects.Properties.SpellScroll import SpellScroll
    from classes.Objects.Properties.Town import Town
    from classes.Objects.Properties.TrivialOwnedObject import TrivialOwnedObject
    from classes.Objects.Properties.WitchHut import WitchHut

class Properties:

    def __init__(self, objects_properties_type: ObjectPropertiesType):
        self.objects_properties_type = objects_properties_type

    def to_dict(self) -> dict:
        return {
            'objects_properties_type': self.get_type(self.objects_properties_type).to_dict()
        }