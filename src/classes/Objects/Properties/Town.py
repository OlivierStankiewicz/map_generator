from classes.Enums.Formation import Formation
from classes.Enums.Heroes import Hero
from classes.Objects.Properties.Helpers.Buildings import Buildings
from classes.Objects.Properties.Helpers.Events import Events
from classes.Objects.Properties.Helpers.Garrison import Garrison
from classes.Objects.Properties.Helpers.MayNotHaveSpell import MayNotHaveSpell
from classes.Objects.Properties.Helpers.MustHaveSpell import MustHaveSpell
from classes.Objects.PropertiesBase import Properties

class Town(Properties):
    @classmethod
    def create_default(cls) -> 'Town':
        return cls(
            absod_id= 0,
            owner= 0,
            name= '',
            garrison= [],
            formation= Formation.SPREAD, # ewentualnie Formation.GROUPED
            buildings= [],
            has_fort= 1, # albo has_fort albo buildings, name i garrison
            must_have_spell= MustHaveSpell.create_default(),
            may_not_have_spell= MayNotHaveSpell.create_default(),
            events= [],
            alignment= 255,
            unknown= [0, 0, 0],
        )

    def __init__(self, absod_id: int, owner: int, name: str, garrison: list[Garrison], formation: Formation,
                 buildings: list[Buildings], has_fort: int, must_have_spell: MustHaveSpell, may_not_have_spell: MayNotHaveSpell,
                 events: list[Events], alignment: int, unknown: list[int]):
        self.absod_id = absod_id
        self.owner = owner
        self.name = name
        self.garrison = garrison
        self.formation = formation
        self.buildings = buildings
        self.has_fort = has_fort
        self.must_have_spell = must_have_spell
        self.may_not_have_spell = may_not_have_spell
        self.events = events
        self.alignment = alignment
        self.unknown = [0, 0, 0]

    def to_dict(self) -> dict:
        result = {
            'absod_id': self.absod_id,
            'owner': self.owner,
            'formation': self.formation.value,
            'has_fort': self.has_fort,
            'must_have_spell': self.must_have_spell.to_dict(),
            'may_not_have_spell': self.may_not_have_spell.to_dict(),
            'events': [event.to_dict() for event in self.events],
            'alignment': self.alignment,
            'unknown': self.unknown,
        }

        if self.name is not None:
            result['name'] = self.name
        if self.garrison is not None:
            result['garrison'] =[garrison.to_dict() for garrison in self.garrison]
        if self.garrison is not None:
            result['garrison'] = [garrison.to_dict() for garrison in self.garrison]
        if self.buildings is not None:
            result['buildings'] = [building.to_dict() for building in self.buildings],

        return result