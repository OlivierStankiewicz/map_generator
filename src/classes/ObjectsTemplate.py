class ObjectsTemplate:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "ObjectsTemplate":
        return cls(
            definition= "AVWmrnd0.def",         #! variable name different than needed for JSON serialization
            passability= [255, 255, 255, 255, 255, 127],
            actionability= [0, 0, 0, 0, 0, 128],
            allowed_landscapes= [255, 0],
            landscape_group= [1, 0],
            object_class= 71, #
            object_subclass= 0,
            object_group= 2, #
            is_ground= 0,
            unknown= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )

    def __init__(self, definition: str, passability: list[int], actionability: list[int], allowed_landscapes: list[int],
                 landscape_group: list[int], object_class: int, object_subclass: int, object_group: int,
                 is_ground: int, unknown: list[int]) -> None:
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

    def to_dict(self) -> dict:
        return {
            "def": self.definition,                 #! variable name changed for JSON serialization
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