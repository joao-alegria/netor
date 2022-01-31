from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, EmbeddedDocumentListField, ListField, MapField, BooleanField, \
    EmbeddedDocumentField
from api.enums.vs_descriptor import SliceManagementControlType, ServiceCreationTimeRange, AvailabilityCoverageRange, \
    ServicePriorityLevel
from api.queries.utils import get_or_error


class ServiceConstraints(EmbeddedDocument):
    sharable = BooleanField()
    can_include_shared_elements = BooleanField()
    priority = StringField(choices=ServicePriorityLevel.get_values())
    preferred_providers = ListField(StringField())
    non_preferred_providers = ListField(StringField())
    prohibited_providers = ListField(StringField())
    atomic_component_id = StringField()


class VsdSla(EmbeddedDocument):
    service_creation_time = StringField(choices=ServiceCreationTimeRange.get_values())
    availability_coverage = StringField(choices=AvailabilityCoverageRange.get_values())
    low_cost_required = BooleanField()


class VsDescriptor(Document):
    vs_descriptor_id = StringField()
    name = StringField()
    version = StringField()
    vs_blueprint_id = StringField()
    management_type = StringField(choices=SliceManagementControlType.get_values())
    qos_parameters = MapField(StringField())
    is_public = BooleanField()
    tenant_id = StringField()
    service_constraints = EmbeddedDocumentListField(ServiceConstraints)
    sla = EmbeddedDocumentField(VsdSla)
    # TODO: Check sliceServiceParameters
    nested_vsd_ids = MapField(StringField())
    associated_vsd_id = StringField()
    domain_id = StringField()

    @classmethod
    def get_or_404(cls, **kwargs):
        return get_or_error(cls, **kwargs)

    @classmethod
    def get_collection(cls):
        return cls._get_collection()