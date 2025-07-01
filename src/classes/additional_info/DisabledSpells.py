class DisabledSpells:

    # no-argument constructor
    @classmethod
    def create_default(cls) -> "DisabledSpells":
        return cls(
            summon_boat= False,
            scuttle_boat= False,
            visions= False,
            view_earth= False,
            disguise= False,
            view_air= False,
            fly= False,
            water_walk= False,
            dimension_door= False,
            town_portal= False,
            quick_sand= False,
            land_mine= False,
            force_field= False,
            fire_wall= False,
            earthquake= False,
            magic_arrow= False,
            ice_bolt= False,
            lightning_bolt= False,
            implosion= False,
            chain_lightning= False,
            frost_ring= False,
            fireball= False,
            inferno= False,
            meteor_shower= False,
            death_ripple= False,
            destroy_undead= False,
            armageddon= False,
            shield= False,
            air_shield= False,
            fire_shield= False,
            protection_from_air= False,
            protection_from_fire= False,
            protection_from_water= False,
            protection_from_earth= False,
            anti_magic= False,
            dispel= False,
            magic_mirror= False,
            cure= False,
            resurrection= False,
            animate_dead= False,
            sacrifice= False,
            bless= False,
            curse= False,
            bloodlust= False,
            precision= False,
            weakness= False,
            stone_skin= False,
            disrupting_ray= False,
            prayer= False,
            mirth= False,
            sorrow= False,
            fortune= False,
            misfortune= False,
            haste= False,
            slow= False,
            slayer= False,
            frenzy= False,
            titans_lightning_bolt= False,
            counterstrike= False,
            berserk= False,
            hypnotize= False,
            forgetfulness= False,
            blind= False,
            teleport= False,
            remove_obstacle= False,
            clone= False,
            fire_elemental= False,
            earth_elemental= False,
            water_elemental= False,
            air_elemental= False,
            padding_70= False,
            padding_71= False
        )

    def __init__(self, summon_boat: bool, scuttle_boat: bool, visions: bool, view_earth: bool, 
                 disguise: bool, view_air: bool, fly: bool, water_walk: bool, dimension_door: bool,
                 town_portal: bool, quick_sand: bool, land_mine: bool, force_field: bool,
                 fire_wall: bool, earthquake: bool, magic_arrow: bool, ice_bolt: bool,
                 lightning_bolt: bool, implosion: bool, chain_lightning: bool, frost_ring: bool,
                 fireball: bool, inferno: bool, meteor_shower: bool, death_ripple: bool,
                 destroy_undead: bool, armageddon: bool, shield: bool, air_shield: bool,
                 fire_shield: bool, protection_from_air: bool, protection_from_fire: bool,
                 protection_from_water: bool, protection_from_earth: bool, anti_magic: bool,
                 dispel: bool, magic_mirror: bool, cure: bool, resurrection: bool,
                 animate_dead: bool, sacrifice: bool, bless: bool, curse: bool,
                 bloodlust: bool, precision: bool, weakness: bool, stone_skin: bool,
                 disrupting_ray: bool, prayer: bool, mirth: bool, sorrow: bool,
                 fortune: bool, misfortune: bool, haste: bool, slow: bool,
                 slayer: bool, frenzy: bool, titans_lightning_bolt:bool,
                 counterstrike :bool , berserk :bool , hypnotize :bool , forgetfulness :bool ,
                 blind :bool , teleport :bool , remove_obstacle :bool , clone :bool ,
                 fire_elemental :bool , earth_elemental :bool , water_elemental :bool ,
                 air_elemental :bool , padding_70 :bool , padding_71 :bool) -> None:
        self.summon_boat= summon_boat
        self.scuttle_boat= scuttle_boat
        self.visions= visions
        self.view_earth= view_earth
        self.disguise= disguise
        self.view_air= view_air
        self.fly= fly
        self.water_walk= water_walk
        self.dimension_door= dimension_door
        self.town_portal= town_portal
        self.quick_sand= quick_sand
        self.land_mine= land_mine
        self.force_field= force_field
        self.fire_wall= fire_wall
        self.earthquake= earthquake
        self.magic_arrow= magic_arrow
        self.ice_bolt= ice_bolt
        self.lightning_bolt= lightning_bolt
        self.implosion= implosion
        self.chain_lightning= chain_lightning
        self.frost_ring= frost_ring
        self.fireball= fireball
        self.inferno= inferno
        self.meteor_shower= meteor_shower
        self.death_ripple= death_ripple
        self.destroy_undead= destroy_undead
        self.armageddon= armageddon
        self.shield= shield
        self.air_shield= air_shield
        self.fire_shield= fire_shield
        self.protection_from_air= protection_from_air
        self.protection_from_fire= protection_from_fire
        self.protection_from_water= protection_from_water
        self.protection_from_earth= protection_from_earth
        self.anti_magic= anti_magic
        self.dispel= dispel
        self.magic_mirror= magic_mirror
        self.cure= cure
        self.resurrection= resurrection
        self.animate_dead= animate_dead
        self.sacrifice= sacrifice
        self.bless= bless
        self.curse= curse
        self.bloodlust= bloodlust
        self.precision= precision
        self.weakness= weakness
        self.stone_skin= stone_skin
        self.disrupting_ray= disrupting_ray
        self.prayer= prayer
        self.mirth= mirth
        self.sorrow= sorrow
        self.fortune= fortune
        self.misfortune= misfortune
        self.haste= haste
        self.slow= slow
        self.slayer= slayer
        self.frenzy= frenzy
        self.titans_lightning_bolt= titans_lightning_bolt
        self.counterstrike= counterstrike
        self.berserk= berserk
        self.hypnotize= hypnotize
        self.forgetfulness= forgetfulness
        self.blind= blind
        self.teleport= teleport
        self.remove_obstacle= remove_obstacle
        self.clone= clone
        self.fire_elemental= fire_elemental
        self.earth_elemental= earth_elemental
        self.water_elemental= water_elemental
        self.air_elemental= air_elemental
        self.padding_70= padding_70
        self.padding_71= padding_71

    def to_dict(self) -> dict:
        return {
            "summon_boat": self.summon_boat,
            "scuttle_boat": self.scuttle_boat,
            "visions": self.visions,
            "view_earth": self.view_earth,
            "disguise": self.disguise,
            "view_air": self.view_air,
            "fly": self.fly,
            "water_walk": self.water_walk,
            "dimension_door": self.dimension_door,
            "town_portal": self.town_portal,
            "quick_sand": self.quick_sand,
            "land_mine": self.land_mine,
            "force_field": self.force_field,
            "fire_wall": self.fire_wall,
            "earthquake": self.earthquake,
            "magic_arrow": self.magic_arrow,
            "ice_bolt": self.ice_bolt,
            "lightning_bolt": self.lightning_bolt,
            "implosion": self.implosion,
            "chain_lightning": self.chain_lightning,
            "frost_ring": self.frost_ring,
            "fireball": self.fireball,
            "inferno": self.inferno,
            "meteor_shower": self.meteor_shower,
            "death_ripple": self.death_ripple,
            "destroy_undead": self.destroy_undead,
            "armageddon": self.armageddon,
            "shield": self.shield,
            "air_shield": self.air_shield,
            "fire_shield": self.fire_shield,
            "protection_from_air": self.protection_from_air,
            "protection_from_fire": self.protection_from_fire,
            "protection_from_water": self.protection_from_water,
            "protection_from_earth": self.protection_from_earth,
            "anti_magic": self.anti_magic,
            "dispel": self.dispel,
            "magic_mirror": self.magic_mirror,
            "cure": self.cure,
            "resurrection": self.resurrection,
            "animate_dead": self.animate_dead,
            "sacrifice": self.sacrifice,
            "bless": self.bless,
            "curse": self.curse,
            "bloodlust": self.bloodlust,
            "precision": self.precision,
            "weakness": self.weakness,
            "stone_skin": self.stone_skin,
            "disrupting_ray": self.disrupting_ray,
            "prayer": self.prayer,
            "mirth": self.mirth,
            "sorrow": self.sorrow,
            "fortune": self.fortune,
            "misfortune": self.misfortune,
            "haste": self.haste,
            "slow": self.slow,
            "slayer": self.slayer,
            "frenzy": self.frenzy,
            "titans_lightning_bolt": self.titans_lightning_bolt,
            "counterstrike": self.counterstrike,
            "berserk": self.berserk,
            "hypnotize": self.hypnotize,
            "forgetfulness": self.forgetfulness,
            "blind": self.blind,
            "teleport": self.teleport,
            "remove_obstacle": self.remove_obstacle,
            "clone": self.clone,
            "fire_elemental": self.fire_elemental,
            "earth_elemental": self.earth_elemental,
            "water_elemental": self.water_elemental,
            "air_elemental": self.air_elemental,
            "padding_70": self.padding_70,
            "padding_71": self.padding_71
        }