class LossCondition:
    def __init__(self):
       self.type = 255

    def __init__(self, type: int):
        self.type = type

    def to_dict(self):
        return {
            "type": self.type
        }