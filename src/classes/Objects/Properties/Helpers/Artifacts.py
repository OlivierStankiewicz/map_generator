class Artifacts(object):
    @classmethod
    def create_default(cls) -> 'Artifacts':
        return cls(
            head = 0,
            shoulders = 0,
            neck = 0,
            right_hand = 0,
            left_hand = 0,
            torso = 0,
            right_ring = 0,
            left_ring = 0,
            feet = 0,
            misc1 = 0,
            misc2 = 0,
            misc3 = 0,
            misc4 = 0,
            misc5 = 0,
            war_machine1 = 0,
            war_machine2 = 0,
            war_machine3 = 0,
            war_machine4 = 0,
            spellbook = 0,
            backpack = []
        )

    def __init__(self, head: int,
				shoulders: int,
				neck: int,
				right_hand: int,
				left_hand: int,
				torso: int,
				right_ring: int,
				left_ring: int,
				feet: int,
				misc1: int,
				misc2: int,
				misc3: int,
				misc4: int,
				misc5: int,
				war_machine1: int,
				war_machine2: int,
				war_machine3: int,
				war_machine4: int,
				spellbook: int,
				backpack: list[int]):
        self.head = head
        self.shoulders = shoulders
        self.neck = neck
        self.right_hand = right_hand
        self.left_hand = left_hand
        self.torso = torso
        self.right_ring = right_ring
        self.left_ring = left_ring
        self.feet = feet
        self.misc1 = misc1
        self.misc2 = misc2
        self.misc3 = misc3
        self.misc4 = misc4
        self.misc5 = misc5
        self.war_machine1 = war_machine1
        self.war_machine2 = war_machine2
        self.war_machine3 = war_machine3
        self.war_machine4 = war_machine4
        self.spellbook = spellbook
        self.backpack = backpack

    def to_dict(self) -> dict:
        return {
            'head' : self.head,
            'shoulders' : self.shoulders,
            'neck' : self.neck,
            'right_hand' : self.right_hand,
            'left_hand' : self.left_hand,
            'torso' : self.torso,
            'right_ring' : self.right_ring,
            'left_ring' : self.left_ring,
            'feet' : self.feet,
            'misc1' : self.misc1,
            'misc2' : self.misc2,
            'misc3' : self.misc3,
            'misc4' : self.misc4,
            'misc5' : self.misc5,
            'war_machine1' : self.war_machine1,
            'war_machine2' : self.war_machine2,
            'war_machine3' : self.war_machine3,
            'backpack' : self.backpack
        }