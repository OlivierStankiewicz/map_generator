from src.classes.Enums.Heroes import Hero
from src.classes.Enums.ObjectPropertiesType import ObjectPropertiesType
from src.classes.Enums.TownType import TownType
from src.classes.Objects import Properties
from src.classes.Objects.Properties.AbandonedMine import AbandonedMine
from src.classes.Objects.Properties.Artifact import Artifact
from src.classes.Objects.Properties.Event import Event
from src.classes.Objects.Properties.Garrison import Garrison
from src.classes.Objects.Properties.Grail import Grail
from src.classes.Objects.Properties.Monster import Monster
from src.classes.Objects.Properties.PandorasBox import PandorasBox
from src.classes.Objects.Properties.PlaceholderHero import PlaceholderHero
from src.classes.Objects.Properties.QuestGuard import QuestGuard
from src.classes.Objects.Properties.RandomDwelling import RandomDwelling
from src.classes.Objects.Properties.RandomDwellingPresetAlignment import RandomDwellingPresetAlignment
from src.classes.Objects.Properties.RandomDwellingPresetLevel import RandomDwellingPresetLevel
from src.classes.Objects.Properties.Resource import Resource
from src.classes.Objects.Properties.Scholar import Scholar
from src.classes.Objects.Properties.SeersHut import SeersHut
from src.classes.Objects.Properties.Shrine import Shrine
from src.classes.Objects.Properties.Sign import Sign
from src.classes.Objects.Properties.SpellScroll import SpellScroll
from src.classes.Objects.Properties.TrivialOwnedObject import TrivialOwnedObject
from src.classes.Objects.Properties.WitchHut import WitchHut
from src.classes.player.Heroes import Heroes


class Objects:
    @classmethod
    def create_default(cls) -> "Objects":
        return cls(
            x=0,
            y=0,
            z=0,
            template_idx=0,
            unknown=[],
            properties=None  # Properties
        )

    def __init__(self, x: int, y: int, z: int,
                 # objectClass: int, objectProperties: int,
                 template_idx: int, unknown: list, properties: Properties) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.template_idx = template_idx
        self.unknown = unknown
        self.properties = properties

    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "template_idx": self.template_idx,
            "unknown": self.unknown,
            "properties": self.properties.to_dict()
        }
