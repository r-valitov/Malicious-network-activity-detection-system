from enum import Enum


class Behavior(Enum):
    TEACH = 0,
    ONLY_SAFE = 1,
    ONLY_DANGER = 2,
    REAL_SIMULATE = 3
