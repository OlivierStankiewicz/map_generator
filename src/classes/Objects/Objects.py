from classes.Objects.PropertiesBase import Properties

class Objects:
    @classmethod
    def create_default(cls) -> "Objects":
        return cls(
            x=0,
            y=0,
            z=0,
            template_idx=0,
            unknown=[],
            properties=Properties.create_default()  # Properties
        )

    def __init__(self, x: int, y: int, z: int,
                 # objectClass: int, objectProperties: int,
                 template_idx: int, unknown: list, properties: Properties) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.template_idx = template_idx
        self.unknown = [0, 0, 0, 0, 0]
        self.properties = properties

    def to_dict(self) -> dict:
        dict = {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "template_idx": self.template_idx,
            "unknown": self.unknown,
        }
        if self.properties is not None:
            dict["properties"] = self.properties if self.properties.__class__ == {}.__class__ else self.properties.to_dict()

        return dict