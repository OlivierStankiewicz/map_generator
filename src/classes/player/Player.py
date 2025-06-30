class Alignment:
    def __init__(self, castle=False, rampart=False, tower=False, inferno=False, necropolis=False,
                 dungeon=False, stronghold=False, fortress=False, conflux=False,
                 padding_9=False, padding_10=False, padding_11=False, padding_12=False,
                 padding_13=False, padding_14=False, padding_15=False):
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

class Player:
    def __init__(self):
        self.can_be_human = 0

    def __init__(self, can_be_human=0, can_be_computer=0, behavior=0, has_customized_alignments=216,
                 allowed_alignments=None, allow_random_alignment=0, main_town=None,
                 has_random_heroes=0, starting_hero=None, num_nonspecific_placeholder_heroes=0, heroes=None):
        self.can_be_human = 0
        self.can_be_computer = 0
        self.behavior = 0
        self.has_customized_alignments = 216
        self.allowed_alignments = allowed_alignments



# {
#       "can_be_human": 0,
#       "can_be_computer": 0,
#       "behavior": 0, // Random
#       "has_customized_alignments": 216,
#       "allowed_alignments": {
#         "castle": false,
#         "rampart": false,
#         "tower": false,
#         "inferno": false,
#         "necropolis": false,
#         "dungeon": false,
#         "stronghold": false,
#         "fortress": false,
#         "conflux": false,
#         "padding_9": false,
#         "padding_10": false,
#         "padding_11": false,
#         "padding_12": false,
#         "padding_13": false,
#         "padding_14": false,
#         "padding_15": false
#       },
#       "allow_random_alignment": 0,
#       // "main_town" field is missing because the player doesn't have a designated main town.
#       "has_random_heroes": 0,
#       "starting_hero": {
#         "type": 255 // (None)
#       },
#       "num_nonspecific_placeholder_heroes": 0,
#       "heroes": []
# },