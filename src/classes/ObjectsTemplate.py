class ObjectsTemplate:
    @classmethod
    def from_default(self):
        self.definition= "AVWmrnd0.def"         #! variable name different than needed for JSON serialization
        self.passability= [255, 255, 255, 255, 255, 127]
        self.actionability= [0, 0, 0, 0, 0, 128]
        self.allowed_landscapes= [255, 0]
        self.landscape_group= [1, 0]
        self.object_class= 71
        self.object_subclass= 0
        self.object_group= 2
        self.is_ground= 0
        self.unknown= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, definition: str, passability: list[int], actionability: list[int], allowed_landscapes: list[int],
                 landscape_group: list[int], object_class: int, object_subclass: int, object_group: int,
                 is_ground: int, unknown: list[int]):
        self.definition = definition
        self.passability = passability
        self.actionability = actionability
        self.allowed_landscapes = allowed_landscapes
        self.landscape_group = landscape_group
        self.object_class = object_class
        self.object_subclass = object_subclass
        self.object_group = object_group
        self.is_ground = is_ground
        self.unknown = unknown

    def to_dict(self):
        return {
            "def": self.definition,             #! variable name changed for JSON serialization
            "passability": self.passability,
            "actionability": self.actionability,
            "allowed_landscapes": self.allowed_landscapes,
            "landscape_group": self.landscape_group,
            "object_class": self.object_class,
            "object_subclass": self.object_subclass,
            "object_group": self.object_group,
            "is_ground": self.is_ground,
            "unknown": self.unknown
        }