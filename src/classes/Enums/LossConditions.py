from enum import Enum

class LossConditions(Enum):
    NORMAL = 255
    LOSE_TOWN = 0
    LOSE_HERO = 1
    TIME_EXPIRES = 2
