from api.enums.utils import AutoName
from enum import auto


class SliceManagementControlType(AutoName):
    PROVIDER_MANAGED = auto()
    TENANT_MANAGED = auto()


class ServiceCreationTimeRange(AutoName):
    SERVICE_CREATION_TIME_LOW = auto()
    SERVICE_CREATION_TIME_MEDIUM = auto()
    UNDEFINED = auto()


class AvailabilityCoverageRange(AutoName):
    AVAILABILITY_COVERAGE_HIGH = auto()
    AVAILABILITY_COVERAGE_MEDIUM = auto()
    UNDEFINED = auto()


class ServicePriorityLevel(AutoName):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
