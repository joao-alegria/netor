from api.enums.utils import AutoName
from enum import auto


class NsScaleType(AutoName):
    SCALE_NS = auto()
    SCALE_VNF = auto()


class ScalingProcedureType(AutoName):
    MANUAL_SCALING = auto()
    AUTOMATED_SCALING = auto()


class LogicOperation(AutoName):
    AND = auto()
    OR = auto()


class RelationalOperation(AutoName):
    GE = auto()
    LE = auto()
    GT = auto()
    LT = auto()
    EQ = auto()
