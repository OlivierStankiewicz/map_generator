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
    @classmethod
    def create_default(cls) -> "Properties":
        return cls(
            objects_properties_type= ObjectPropertiesType.ABANDONED_MINE
        )

    def __init__(self, objects_properties_type: ObjectPropertiesType):
        self.objects_properties_type = objects_properties_type

    def to_dict(self) -> dict:
        return {
            'objects_properties_type': self.get_type(self.objects_properties_type).to_dict()
        }

    @classmethod
    def get_type(cls, type: ObjectPropertiesType):
        if type == ObjectPropertiesType.GENERIC_NO_PROPERTIES:
            return None
        elif type == ObjectPropertiesType.ABANDONED_MINE:
            # Lazy import inside the method
            from classes.Objects.Properties.AbandonedMine import AbandonedMine
            return AbandonedMine.create_default()
        elif type == ObjectPropertiesType.ARTIFACT:
            # Lazy import inside the method
            from classes.Objects.Properties.Artifact import Artifact
            return Artifact.create_default()
        elif type == ObjectPropertiesType.EVENT:
            # Lazy import inside the method
            from classes.Objects.Properties.Event import Event
            return Event.create_default()
        elif type == ObjectPropertiesType.GARRISON:
            # Lazy import inside the method
            from classes.Objects.Properties.Garrison import Garrison
            return Garrison.create_default()
        elif type == ObjectPropertiesType.GRAIL:
            # Lazy import inside the method
            from classes.Objects.Properties.Grail import Grail
            return Grail.create_default()
        elif type == ObjectPropertiesType.HERO:
            # Lazy import inside the method
            from classes.Objects.Properties.Hero import Hero
            return Hero.create_default()
        elif type == ObjectPropertiesType.MONSTER:
            # Lazy import inside the method
            from classes.Objects.Properties.Monster import Monster
            return Monster.create_default()
        elif type == ObjectPropertiesType.PANDORAS_BOX:
            # Lazy import inside the method
            from classes.Objects.Properties.PandorasBox import PandorasBox
            return PandorasBox.create_default()
        elif type == ObjectPropertiesType.PLACEHOLDER_HERO:
            # Lazy import inside the method
            from classes.Objects.Properties.PlaceholderHero import PlaceholderHero
            return PlaceholderHero.create_default()
        elif type == ObjectPropertiesType.QUEST_GUARD:
            # Lazy import inside the method
            from classes.Objects.Properties.QuestGuard import QuestGuard
            return QuestGuard.create_default()
        elif type == ObjectPropertiesType.RANDOM_DWELLING:
            # Lazy import inside the method
            from classes.Objects.Properties.RandomDwelling import RandomDwelling
            return RandomDwelling.create_default()
        elif type == ObjectPropertiesType.RANDOM_DWELLING_PRESET_ALIGNMENT:
            # Lazy import inside the method
            from classes.Objects.Properties.RandomDwellingPresetAlignment import RandomDwellingPresetAlignment
            return RandomDwellingPresetAlignment.create_default()
        elif type == ObjectPropertiesType.RANDOM_DWELLING_PRESET_LEVEL:
            # Lazy import inside the method
            from classes.Objects.Properties.RandomDwellingPresetLevel import RandomDwellingPresetLevel
            return RandomDwellingPresetLevel.create_default()
        elif type == ObjectPropertiesType.RESOURCE:
            # Lazy import inside the method
            from classes.Objects.Properties.Resource import Resource
            return Resource.create_default()
        elif type == ObjectPropertiesType.SCHOLAR:
            # Lazy import inside the method
            from classes.Objects.Properties.Scholar import Scholar
            return Scholar.create_default()
        elif type == ObjectPropertiesType.SEERS_HUT:
            # Lazy import inside the method
            from classes.Objects.Properties.SeersHut import SeersHut
            return SeersHut.create_default()
        elif type == ObjectPropertiesType.SHRINE:
            # Lazy import inside the method
            from classes.Objects.Properties.Shrine import Shrine
            return Shrine.create_default()
        elif type == ObjectPropertiesType.SIGN:
            # Lazy import inside the method
            from classes.Objects.Properties.Sign import Sign
            return Sign.create_default()
        elif type == ObjectPropertiesType.SPELL_SCROLL:
            # Lazy import inside the method
            from classes.Objects.Properties.SpellScroll import SpellScroll
            return SpellScroll.create_default()
        elif type == ObjectPropertiesType.TOWN:
            # Lazy import inside the method
            from classes.Objects.Properties.Town import Town
            return Town.create_default()
        elif type == ObjectPropertiesType.TRIVIAL_OWNED_OBJECT:
            # Lazy import inside the method
            from classes.Objects.Properties.TrivialOwnedObject import TrivialOwnedObject
            return TrivialOwnedObject.create_default()
        elif type == ObjectPropertiesType.WITCH_HUT:
            # Lazy import inside the method
            from classes.Objects.Properties.WitchHut import WitchHut
            return WitchHut.create_default()
        else:
            raise Exception(f"Unknown type: {type}")