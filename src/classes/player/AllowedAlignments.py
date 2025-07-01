class AllowedAlignments:

    # alternative no-argument constructor
    @classmethod
    def create_default(cls):
        return cls(
            castle = False,
            rampart = False,
            tower = False,
            inferno = False,
            necropolis = False,
            dungeon = False,
            stronghold = False,
            fortress = False,
            conflux = False,
            padding_9 = False,
            padding_10 = False,
            padding_11 = False,
            padding_12 = False,
            padding_13 = False,
            padding_14 = False,
            padding_15 = False
        )
    
    def __init__(self, castle: bool, rampart: bool, tower: bool, inferno: bool, necropolis: bool,
                 dungeon: bool, stronghold: bool, fortress: bool, conflux: bool,
                 padding_9: bool, padding_10: bool, padding_11: bool, padding_12: bool,
                 padding_13: bool, padding_14: bool, padding_15: bool):
        self.castle = castle
        self.rampart = rampart
        self.tower = tower
        self.inferno = inferno
        self.necropolis = necropolis
        self.dungeon = dungeon
        self.stronghold = stronghold
        self.fortress = fortress
        self.conflux = conflux
        self.padding_9 = padding_9
        self.padding_10 = padding_10
        self.padding_11 = padding_11
        self.padding_12 = padding_12
        self.padding_13 = padding_13
        self.padding_14 = padding_14
        self.padding_15 = padding_15

    def to_dict(self):
        return {
            "castle": self.castle,
            "rampart": self.rampart,
            "tower": self.tower,
            "inferno": self.inferno,
            "necropolis": self.necropolis,
            "dungeon": self.dungeon,
            "stronghold": self.stronghold,
            "fortress": self.fortress,
            "conflux": self.conflux,
            "padding_9": self.padding_9,
            "padding_10": self.padding_10,
            "padding_11": self.padding_11,
            "padding_12": self.padding_12,
            "padding_13": self.padding_13,
            "padding_14": self.padding_14,
            "padding_15": self.padding_15
        }