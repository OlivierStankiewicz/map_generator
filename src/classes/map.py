from classes.BasicInfo import BasicInfo
from classes.player.Player import Player
from classes.additional_info.AdditionalInfo import AdditionalInfo
from classes.tile.Tile import Tile
from classes.ObjectsTemplate import ObjectsTemplate

# possible number of tiles: 10368 (72x72x2) / 36x36, / 108x108, / 144x144

class Map:
    @classmethod
    def from_default(self):
        self.format = 28
        self.basic_info = BasicInfo.from_default()
        self.players = [Player.from_default() for _ in range(8)]
        self.additional_info = AdditionalInfo.from_default()
        self.tiles = [Tile.from_default() for _ in range(10368)]
        self.objects_templates = [ObjectsTemplate.from_default()]
        self.objects = []
        self.global_events = []
        self.padding = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, format: int, basic_info: BasicInfo, players: list[Player],
                 additional_info: AdditionalInfo, tiles: list[Tile], objects_templates: list[ObjectsTemplate],
                 objects: list, global_events: list, padding: list[int]):
        self.format = format
        self.basic_info = basic_info
        self.players = players
        self.additional_info = additional_info
        self.tiles = tiles
        self.objects_templates = objects_templates
        self.objects = objects
        self.global_events = global_events
        self.padding = padding

    def to_dict(self):
        return {
            "format": self.format,
            "basic_info": self.basic_info.to_dict(),
            "players": [player.to_dict() for player in self.players],
            "additional_info": self.additional_info.to_dict(),
            "tiles": [tile.to_dict() for tile in self.tiles],
            "objects_templates": [template.to_dict() for template in self.objects_templates],
            "objects": [obj for obj in self.objects],
            "global_events": self.global_events,
            "padding": self.padding
        }