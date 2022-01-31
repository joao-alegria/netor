from api.enums.utils import AutoName
from enum import auto


class UEMobilityLevel(AutoName):
    STATIONARY = auto()
    NOMADIC = auto()
    RESTRICTED_MOBILITY = auto()
    FULLY_MOBILITY = auto()


class SliceType(AutoName):
    EMBB = auto()
    URLLC = auto()


class NsstType(AutoName):
    NONE = auto()
    RAN = auto()
    CORE = auto()
    EHEALTH = auto()
