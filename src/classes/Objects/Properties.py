from src.classes.Enums.ObjectPropertiesType import ObjectPropertiesType


class Properties:
    @classmethod
    def create_default(cls) -> "Properties":
        return cls(
            objectsPropertiesType= None
        )

    def __init__(self, objectsPropertiesType: ObjectPropertiesType):
        self.objectsPropertiesType = objectsPropertiesType

    def to_dict(self) -> dict:
        return {}