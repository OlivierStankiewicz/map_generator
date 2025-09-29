from src.classes.Objects import Properties


class Objects:
    @classmethod
    def create_default(cls) -> "Objects":
        return cls(
            x= 0,
            y= 0,
            z= 0,
            template_idx= 0,
            unknown= [],
            properties= None
        )

    def __init__(self, x: int, y: int, z: int,
                 #objectClass: int, objectProperties: int,
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
