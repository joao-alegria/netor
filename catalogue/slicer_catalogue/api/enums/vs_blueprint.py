from api.enums.utils import AutoName
from enum import auto


class VsComponentPlacement(AutoName):
    EDGE = auto()
    CLOUD = auto()


class VsComponentType(AutoName):
    SERVICE = auto()
    FUNCTION = auto()
    OTHER = auto()


class MetricCollectionType(AutoName):
    CUMULATIVE = auto()
    DELTA = auto()
    GAUGE = auto()


class SliceServiceType(AutoName):
    NONE = auto()
    EMBB = auto()
    URLLC = auto()
    M_IOT = auto()
    ENTERPRISE = auto()
    NFV_IAAS = auto()


class EMBBServiceCategory(AutoName):
    URBAN_MACRO = auto()
    RURAL_MACRO = auto()
    INDOOR_HOTSPOT = auto()
    BROADBAND_ACCESS_IN_A_CROWD = auto()
    DENSE_URBAN = auto()
    BROADBAND_LIKE_SERVICES = auto()
    HIGH_SPEED_TRAIN = auto()
    HIGH_SPEED_VEHICLE = auto()
    AIRPLANES_CONNECTIVITY = auto()


class URLLCServiceCategory(AutoName):
    DISCRETE_AUTOMATION = auto()
    PROCESS_AUTOMATION_REMOTE_CONTROL = auto()
    PROCESS_AUTOMATION_MONITORING = auto()
    ELECTRICITY_DISTRIBUTION_HIGH_VOLTAGE = auto()
    ELECTRICITY_DISTRIBUTION_MEDIUM_VOLTAGE = auto()
    INTELLIGENT_TRANSPORT_SYSTEMS_INFRASTRUCTURE_BACKHAUL = auto()


class VsbActionsParametersValueTypes(AutoName):
    STRING = auto()
    INTEGER = auto()
    BOOLEAN = auto()
