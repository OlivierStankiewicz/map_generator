from classes.Enums.ObjectPropertiesType import ObjectPropertiesType

class Properties:
    @classmethod
    def create_default(cls) -> "Properties":
        return cls(
            objects_properties_type= ObjectPropertiesType.ABANDONED_MINE
        )

    def __init__(self, objects_properties_type: ObjectPropertiesType):
        self.objects_properties_type = objects_properties_type

    def to_dict(self) -> dict:
        return {}

    # def get_type(self, type: int):
    #     if type == ObjectPropertiesType.GENERIC_NO_PROPERTIES:
    #         return self.create_default()
    #     elif type == ObjectPropertiesType.ABANDONED_MINE:
    #         return AbandonedMine.create_default()
    #     elif type == ObjectPropertiesType.ARTIFACT:
    #         return Artifact.create_default()
    #     elif type == ObjectPropertiesType.EVENT:
    #         return Event.create_default()
    #     elif type == ObjectPropertiesType.GARRISON:
    #         return Garrison.create_default()
    #     elif type == ObjectPropertiesType.GRAIL:
    #         return Grail.create_default()
    #     elif type == ObjectPropertiesType.HERO:
    #         return Hero.create_default()
    #     elif type == ObjectPropertiesType.MONSTER:
    #         return Monster.create_default()
    #     elif type == ObjectPropertiesType.PANDORAS_BOX:
    #         return PandorasBox.create_default()
    #     elif type == ObjectPropertiesType.PLACEHOLDER_HERO:
    #         return PlaceholderHero.create_default()
    #     elif type == ObjectPropertiesType.QUEST_GUARD:
    #         return QuestGuard.create_default()
    #     elif type == ObjectPropertiesType.RANDOM_DWELLING:
    #         return RandomDwelling.create_default()
    #     elif type == ObjectPropertiesType.RANDOM_DWELLING_PRESET_ALIGNMENT:
    #         return RandomDwellingPresetAlignment.create_default()
    #     elif type == ObjectPropertiesType.RANDOM_DWELLING_PRESET_LEVEL:
    #         return RandomDwellingPresetLevel.create_default()
    #     elif type == ObjectPropertiesType.RESOURCE:
    #         return Resource.create_default()
    #     elif type == ObjectPropertiesType.SCHOLAR:
    #         return Scholar.create_default()
    #     elif type == ObjectPropertiesType.SEERS_HUT:
    #         return SeersHut.create_default()
    #     elif type == ObjectPropertiesType.SHRINE:
    #         return Shrine.create_default()
    #     elif type == ObjectPropertiesType.SIGN:
    #         return Sign.create_default()
    #     elif type == ObjectPropertiesType.SPELL_SCROLL:
    #         return SpellScroll.create_default()
    #     elif type == ObjectPropertiesType.TOWN:
    #         return Town.create_default()
    #     elif type == ObjectPropertiesType.TRIVIAL_OWNED_OBJECT:
    #         return TrivialOwnedObject.create_default()
    #     elif type == ObjectPropertiesType.WITCH_HUT:
    #         return WitchHut.create_default()
    #     else:
    #         raise Exception(f"Unknown type: {type}")