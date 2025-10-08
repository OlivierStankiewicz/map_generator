from classes.BasicInfo import BasicInfo
from classes.player.Player import Player
from classes.additional_info.AdditionalInfo import AdditionalInfo
from classes.tile.Tile import Tile
from classes.ObjectsTemplate import ObjectsTemplate
from classes.Objects.Objects import Objects

# possible number of tiles: 10368 (72x72x2) / 36x36, / 108x108, / 144x144

class Map:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "Map":
        return cls(
            format= 28,
            basic_info= BasicInfo.create_default(),
            players= [Player.create_default() for _ in range(8)],
            additional_info= AdditionalInfo.create_default(),
            tiles= [Tile.create_default() for _ in range(10368)],
            objects_templates = [ObjectsTemplate.create_default()],
            objects= [Objects.create_default()],
            global_events= [],
            padding= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )

    def __init__(self, format: int, basic_info: BasicInfo, players: list[Player],
                 additional_info: AdditionalInfo, tiles: list[Tile], objects_templates: list[ObjectsTemplate],
                 objects: list, global_events: list, padding: list[int]) -> None:
        self.format = format
        self.basic_info = basic_info
        self.players = players
        self.additional_info = additional_info
        self.tiles = tiles
        self.objects_templates = objects_templates
        self.objects = objects
        self.global_events = global_events
        self.padding = padding

    def to_dict(self) -> dict:
        return {
            "format": self.format,
            "basic_info": self.basic_info.to_dict(),
            "players": [player.to_dict() for player in self.players],
            "additional_info": self.additional_info.to_dict(),
            "tiles": [tile.to_dict() for tile in self.tiles],
            "objects_templates": [template.to_dict() for template in self.objects_templates],
            "objects": [self.objects],
            "global_events": self.global_events,
            "padding": self.padding
        }