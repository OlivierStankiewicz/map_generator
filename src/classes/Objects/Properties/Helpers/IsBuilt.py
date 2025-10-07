class IsBuilt:
    @classmethod
    def create_default(cls) -> 'IsBuilt':
        return cls(
            city_hall = False,
            capitol = False,
            fort = False,
            citadel = False,
            castle = False,
            tavern = False,
            blacksmith = False,
            marketplace = False,
            resource_silo = False,
            artifact_merchants = False,
            mage_guild_1 = False,
            mage_guild_2 = False,
            mage_guild_3 = False,
            mage_guild_4 = False,
            mage_guild_5 = False,
            shipyard = False,
            grail = False,
            special_building_1 = False,
            special_building_2 = False,
            special_building_3 = False,
            special_building_4 = False,
            dwelling_1 = False,
            dwelling_1u = False,
            horde_1 = False,
            dwelling_2 = False,
            dwelling_2u = False,
            horde_2 = False,
            dwelling_3 = False,
            dwelling_3u = False,
            horde_3 = False,
            dwelling_4 = False,
            dwelling_4u = False,
            horde_4 = False,
            dwelling_5 = False,
            dwelling_5u = False,
            horde_5 = False,
            dwelling_6 = False,
            dwelling_6u = False,
            dwelling_7 = False,
            dwelling_7u = False,
            padding_41 = False,
            padding_42 = False,
            padding_43 = False,
            padding_44 = False,
            padding_45 = False,
            padding_46 = False,
            padding_47 = False
        )

    def __init__(self, town_hall: bool,
					city_hall: bool,
					capitol: bool,
					fort: bool,
					citadel: bool,
					castle: bool,
					tavern: bool,
					blacksmith: bool,
					marketplace: bool,
					resource_silo: bool,
					artifact_merchants: bool,
					mage_guild_1: bool,
					mage_guild_2: bool,
					mage_guild_3: bool,
					mage_guild_4: bool,
					mage_guild_5: bool,
					shipyard: bool,
					grail: bool,
					special_building_1: bool,
					special_building_2: bool,
					special_building_3: bool,
					special_building_4: bool,
					dwelling_1: bool,
					dwelling_1u: bool,
					horde_1: bool,
					dwelling_2: bool,
					dwelling_2u: bool,
					horde_2: bool,
					dwelling_3: bool,
					dwelling_3u: bool,
					horde_3: bool,
					dwelling_4: bool,
					dwelling_4u: bool,
					horde_4: bool,
					dwelling_5: bool,
					dwelling_5u: bool,
					horde_5: bool,
					dwelling_6: bool,
					dwelling_6u: bool,
					dwelling_7: bool,
					dwelling_7u: bool,
					padding_41: bool,
					padding_42: bool,
					padding_43: bool,
					padding_44: bool,
					padding_45: bool,
					padding_46: bool,
					padding_47: bool) -> None:
        self.town_hall = town_hall
        self.city_hall = city_hall
        self.capitol = capitol
        self.fort = fort
        self.citadel = citadel
        self.castle = castle
        self.tavern = tavern
        self.blacksmith = blacksmith
        self.marketplace = marketplace
        self.resource_silo = resource_silo
        self.artifact_merchants = artifact_merchants
        self.mage_guild_1 = mage_guild_1
        self.mage_guild_2 = mage_guild_2
        self.mage_guild_3 = mage_guild_3
        self.mage_guild_4 = mage_guild_4
        self.mage_guild_5 = mage_guild_5
        self.shipyard = shipyard
        self.grail = grail
        self.special_building_1 = special_building_1
        self.special_building_2 = special_building_2
        self.special_building_3 = special_building_3
        self.special_building_4 = special_building_4
        self.dwelling_1 = dwelling_1
        self.dwelling_1u = dwelling_1u
        self.horde_1 = horde_1
        self.dwelling_2 = dwelling_2
        self.dwelling_2u = dwelling_2u
        self.horde_2 = horde_2
        self.dwelling_3 = dwelling_3
        self.dwelling_3u = dwelling_3u
        self.horde_3 = horde_3
        self.dwelling_4 = dwelling_4
        self.dwelling_4u = dwelling_4u
        self.horde_4 = horde_4
        self.dwelling_5 = dwelling_5
        self.dwelling_5u = dwelling_5u
        self.horde_5 = horde_5
        self.dwelling_6 = dwelling_6
        self.dwelling_6u = dwelling_6u
        self.dwelling_7 = dwelling_7
        self.dwelling_7u = dwelling_7u
        self.padding_41 = padding_41
        self.padding_42 = padding_42
        self.padding_43 = padding_43
        self.padding_44 = padding_44
        self.padding_45 = padding_45
        self.padding_46 = padding_46
        self.padding_47 = padding_47


    def to_dict(self) -> dict:
        return {
            "town_hall": self.town_hall,
            "city_hall": self.city_hall,
            "capitol": self.capitol,
            "fort": self.fort,
            "citadel": self.citadel,
            "castle": self.castle,
            "tavern": self.tavern,
            "blacksmith": self.blacksmith,
            "marketplace": self.marketplace,
            "resource_silo": self.resource_silo,
            "artifact_merchants": self.artifact_merchants,
            "mage_guild_1": self.mage_guild_1,
            "mage_guild_2": self.mage_guild_2,
            "mage_guild_3": self.mage_guild_3,
            "mage_guild_4": self.mage_guild_4,
            "mage_guild_5": self.mage_guild_5,
            "shipyard": self.shipyard,
            "grail": self.grail,
            "special_building_1": self.special_building_1,
            "special_building_2": self.special_building_2,
            "special_building_3": self.special_building_3,
            "special_building_4": self.special_building_4,
            "dwelling_1": self.dwelling_1,
            "dwelling_1u": self.dwelling_1u,
            "horde_1": self.horde_1,
            "dwelling_2": self.dwelling_2,
            "dwelling_2u": self.dwelling_2u,
            "horde_2": self.horde_2,
            "dwelling_3": self.dwelling_3,
            "dwelling_3u": self.dwelling_3u,
            "horde_3": self.horde_3,
            "dwelling_4": self.dwelling_4,
            "dwelling_4u": self.dwelling_4u,
            "horde_4": self.horde_4,
            "dwelling_5": self.dwelling_5,
            "dwelling_5u": self.dwelling_5u,
            "horde_5": self.horde_5,
            "dwelling_6": self.dwelling_6,
            "dwelling_6u": self.dwelling_6u,
            "dwelling_7": self.dwelling_7,
            "dwelling_7u": self.dwelling_7u,
            "padding_41": self.padding_41,
            "padding_42": self.padding_42,
            "padding_43": self.padding_43,
            "padding_44": self.padding_44,
            "padding_45": self.padding_45,
            "padding_46": self.padding_46,
            "padding_47": self.padding_47
        }