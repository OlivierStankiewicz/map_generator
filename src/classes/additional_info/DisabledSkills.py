class DisabledSkills:
    @classmethod
    def from_default(self):
        self.pathfinding= False
        self.archery= False
        self.logistics= False
        self.scouting= False
        self.diplomacy= False
        self.navigation= False
        self.leadership= False
        self.wisdom= False
        self.mysticism= False
        self.luck= False
        self.ballistics= False
        self.eagle_eye= False
        self.necromancy= False
        self.estates= False
        self.fire_magic= False
        self.air_magic= False
        self.water_magic= False
        self.earth_magic= False
        self.scholar= False
        self.tactics= False
        self.artillery= False
        self.learning= False
        self.offense= False
        self.armorer= False
        self.intelligence= False
        self.sorcery= False
        self.resistance= False
        self.first_aid= False
        self.padding_28= False
        self.padding_29= False
        self.padding_30= False
        self.padding_31= False

    def __init__(self, pathfinding: bool, archery: bool, logistics: bool, scouting: bool,
                 diplomacy: bool, navigation: bool, leadership: bool, wisdom: bool,
                 mysticism: bool, luck: bool, ballistics: bool, eagle_eye: bool,
                 necromancy: bool, estates: bool, fire_magic: bool, air_magic: bool,
                 water_magic: bool, earth_magic: bool, scholar: bool, tactics: bool,
                 artillery: bool, learning: bool, offense: bool, armorer: bool,
                 intelligence: bool, sorcery: bool, resistance: bool,
                 first_aid: bool, padding_28: bool, padding_29: bool,
                 padding_30: bool, padding_31: bool):
        self.pathfinding= pathfinding
        self.archery= archery
        self.logistics= logistics
        self.scouting= scouting
        self.diplomacy= diplomacy
        self.navigation= navigation
        self.leadership= leadership
        self.wisdom= wisdom
        self.mysticism= mysticism
        self.luck= luck
        self.ballistics= ballistics
        self.eagle_eye= eagle_eye
        self.necromancy= necromancy
        self.estates= estates
        self.fire_magic= fire_magic
        self.air_magic= air_magic
        self.water_magic= water_magic
        self.earth_magic= earth_magic
        self.scholar= scholar
        self.tactics= tactics
        self.artillery= artillery
        self.learning= learning
        self.offense= offense
        self.armorer= armorer
        self.intelligence= intelligence
        self.sorcery= sorcery
        self.resistance= resistance
        self.first_aid= first_aid
        self.padding_28= padding_28
        self.padding_29= padding_29
        self.padding_30= padding_30
        self.padding_31= padding_31

    def to_dict(self):
        return {
            "pathfinding": self.pathfinding,
            "archery": self.archery,
            "logistics": self.logistics,
            "scouting": self.scouting,
            "diplomacy": self.diplomacy,
            "navigation": self.navigation,
            "leadership": self.leadership,
            "wisdom": self.wisdom,
            "mysticism": self.mysticism,
            "luck": self.luck,
            "ballistics": self.ballistics,
            "eagle_eye": self.eagle_eye,
            "necromancy": self.necromancy,
            "estates": self.estates,
            "fire_magic": self.fire_magic,
            "air_magic": self.air_magic,
            "water_magic": self.water_magic,
            "earth_magic": self.earth_magic,
            "scholar": self.scholar,
            "tactics": self.tactics,
            "artillery": self.artillery,
            "learning": self.learning,
            "offense": self.offense,
            "armorer": self.armorer,
            "intelligence": self.intelligence,
            "sorcery": self.sorcery,
            "resistance": self.resistance,
            "first_aid": self.first_aid,
            "padding_28": self.padding_28,
            "padding_29": self.padding_29,
            "padding_30": self.padding_30,
            "padding_31": self.padding_31
        }