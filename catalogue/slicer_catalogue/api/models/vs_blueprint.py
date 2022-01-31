from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, IntField, EmbeddedDocumentListField, ListField, MapField, BooleanField
from api.enums.vs_blueprint import VsComponentPlacement, VsbActionsParametersValueTypes, VsComponentType, \
    MetricCollectionType, SliceServiceType, \
    EMBBServiceCategory, URLLCServiceCategory
from api.queries.utils import get_or_error


# vnfPackages
class VsdParameterValueRange(EmbeddedDocument):
    parameter_id = StringField()
    min_value = IntField()
    max_value = IntField()


class VsdNsdTranslationRule(Document):
    input = EmbeddedDocumentListField(VsdParameterValueRange)
    blueprint_id = StringField()
    nst_id = StringField()
    nsd_id = StringField()
    nsd_version = StringField()
    ns_flavour_id = StringField()
    ns_instantiation_level_id = StringField()
    nsd_info_id = StringField()

    @classmethod
    def get_or_404(cls, **kwargs):
        return get_or_error(cls, **kwargs)

    @classmethod
    def get_collection(cls):
        return cls._get_collection()


class VsbActionsParameters(EmbeddedDocument):
    parameter_id = StringField()
    parameter_name = StringField()
    parameter_type = StringField(choices=VsbActionsParametersValueTypes.get_values())
    parameter_default_value = StringField()


class VsbActions(Document):
    parameters = EmbeddedDocumentListField(VsbActionsParameters)
    blueprint_id = StringField()
    action_id = StringField()
    action_name = StringField()

    @classmethod
    def get_or_404(cls, **kwargs):
        return get_or_error(cls, **kwargs)

    @classmethod
    def get_collection(cls):
        return cls._get_collection()


# vsBlueprint
class VsBlueprintParameter(EmbeddedDocument):
    parameter_id = StringField()
    parameter_name = StringField()
    parameter_type = StringField()
    parameter_description = StringField()
    applicability_field = StringField()


class VsComponent(EmbeddedDocument):
    component_id = StringField()
    servers_number = IntField()
    image_urls = ListField(StringField())
    end_points_ids = ListField(StringField())
    lifecycleOperations = MapField(StringField())
    placement = StringField(choices=VsComponentPlacement.get_values())  # EnumField(VsComponentPlacement)
    type = StringField(choices=VsComponentType.get_values())  # EnumField(VsComponentType)
    associated_vsb_id = StringField()
    compatible_site = StringField()


class VsbForwardingPathEndPoint(EmbeddedDocument):
    vs_component_id = StringField()
    endPoint_id = StringField()


class VsbEndpoint(EmbeddedDocument):
    end_point_id = StringField()
    external = BooleanField()
    management = BooleanField()
    ran_connection = BooleanField()


class VsbLink(EmbeddedDocument):
    end_point_ids = ListField(StringField())
    external = BooleanField()
    name = StringField()
    connectivity_properties = ListField(StringField())


class ApplicationMetric(EmbeddedDocument):
    topic = StringField()
    metric_id = StringField()
    name = StringField()
    metric_collection_type = StringField(choices=MetricCollectionType.get_values())  # EnumField(MetricCollectionType)
    unit = StringField()
    interval = StringField()


class VsBlueprint(Document):
    blueprint_id = StringField()
    version = StringField()
    name = StringField()
    description = StringField()
    parameters = EmbeddedDocumentListField(VsBlueprintParameter)
    atomic_components = EmbeddedDocumentListField(VsComponent)
    service_sequence = EmbeddedDocumentListField(VsbForwardingPathEndPoint)
    end_points = EmbeddedDocumentListField(VsbEndpoint)
    connectivity_services = EmbeddedDocumentListField(VsbLink)
    configurable_parameters = ListField(StringField())
    application_metrics = EmbeddedDocumentListField(ApplicationMetric)
    inter_site = BooleanField()
    slice_service_type = StringField(choices=SliceServiceType.get_values())  # EnumField(SliceServiceType)
    embb_service_category = StringField(choices=EMBBServiceCategory.get_values())  # EnumField(EMBBServiceCategory)
    urllc_service_category = StringField(choices=URLLCServiceCategory.get_values())  # EnumField(URLLCServiceCategory)

    @classmethod
    def get_or_404(cls, **kwargs):
        return get_or_error(cls, **kwargs)

    @classmethod
    def get_collection(cls):
        return cls._get_collection()


# VsBlueprintInfo
class VsBlueprintInfo(Document):
    vs_blueprint_id = StringField()
    vs_blueprint_version = StringField()
    name = StringField()
    owner = StringField()
    on_boarded_nsd_info_id = ListField(StringField())
    on_boarded_nst_info_id = ListField(StringField())
    on_boarded_vnf_package_info_id = ListField(StringField())
    on_boarded_mec_app_package_info_id = ListField(StringField())
    active_vsd_id = ListField(StringField())

    @classmethod
    def get_or_404(cls, **kwargs):
        return get_or_error(cls, **kwargs)

    @classmethod
    def get_collection(cls):
        return cls._get_collection()
