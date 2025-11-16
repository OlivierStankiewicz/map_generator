class Artifacts(object):
    @classmethod
    def create_default(cls) -> 'Artifacts':
        return cls(
            head = 65535,
            shoulders = 65535,
            neck = 65535,
            right_hand = 65535,
            left_hand = 65535,
            torso = 65535,
            right_ring = 65535,
            left_ring = 65535,
            feet = 65535,
            misc1 = 65535,
            misc2 = 65535,
            misc3 = 65535,
            misc4 = 65535,
            misc5 = 65535,
            war_machine1 = 65535,
            war_machine2 = 65535,
            war_machine3 = 65535,
            war_machine4 = 65535,
            spellbook = 65535,
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
            'war_machine4' : self.war_machine4,
            'spellbook' : self.spellbook,
            'backpack' : self.backpack
        }