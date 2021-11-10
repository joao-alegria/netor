from marshmallow import Schema, ValidationError, pre_load, validate
from marshmallow.fields import String, List, Boolean, Integer, Dict, Nested
from api.enums.vs_blueprint import VsbActionsParametersValueTypes, SliceServiceType, EMBBServiceCategory, \
    URLLCServiceCategory, MetricCollectionType, \
    VsComponentPlacement, VsComponentType


class VsdParameterValueRangeSerializer(Schema):
    parameter_id = String(required=True, error_messages={"required": "VSD parameter value range without ID."})
    min_value = Integer()
    max_value = Integer()


class VsdNsdTranslationRuleSerializer(Schema):
    input = List(Nested(VsdParameterValueRangeSerializer))
    blueprint_id = String()
    nst_id = String()
    nsd_id = String()
    nsd_version = String()
    ns_flavour_id = String()
    ns_instantiation_level_id = String()
    nsd_info_id = String()

    @pre_load
    def is_valid(self, data, **kwargs):

        if len(data.get('input', [])) == 0:
            raise ValidationError("VSD NSD translation rule without matching conditions", "input")

        elif data.get('nst_id') is None and data.get('nsd_id') is None:
            raise ValidationError("VSD NSD translation rule without NSD ID/NST ID", "nst_id & nsd_id")

        elif data.get('nsd_id') is not None and data.get('nsd_version') is None:
            raise ValidationError("VSD NSD translation rule without NSD version", "nsd_id & nsd_version")

        return data


class VsbActionsParametersSerializer(Schema):
    parameter_id = String(required=True, error_messages={"required": "VSD parameter value range without ID."})
    parameter_name = String()
    parameter_type = String(validate=validate.OneOf(VsbActionsParametersValueTypes.get_values()))
    parameter_default_value = String()


class VsbActionsSerializer(Schema):
    parameters = List(Nested(VsbActionsParametersSerializer))
    blueprint_id = String()
    action_id = String()
    action_name = String()


class VsBlueprintParameterSerializer(Schema):
    parameter_id = String(required=True, error_messages={"required": "VS blueprint parameter without ID"})
    parameter_name = String()
    parameter_type = String()
    parameter_description = String()
    applicability_field = String()


class VsComponentSerializer(Schema):
    component_id = String(required=True, error_messages={"required": "VSB atomic component without ID."})
    servers_number = Integer()
    image_urls = List(String())
    end_points_ids = List(String())
    lifecycleOperations = Dict(keys=String(), values=String())
    placement = String(validate=validate.OneOf(VsComponentPlacement.get_values()))
    type = String(validate=validate.OneOf(VsComponentType.get_values()))
    associated_vsb_id = String()
    compatible_site = String()

    @pre_load
    def is_valid(self, data, **kwargs):
        if data.get('type') == VsComponentType.SERVICE.value and data.get('associated_vsb_id') is None:
            raise ValidationError("Component of type service without associated VSB id", "type & associated_vsb_id")
        return data


class VsbForwardingPathEndPointSerializer(Schema):
    vs_component_id = String(required=True,
                             error_messages={"required": "VS Forwarding Graph element without VS component"})
    end_point_id = String(required=True, error_messages={"required": "VS Forwarding Graph element without end point"})


class VsbForwardingPathHopSerializer(Schema):
    hop_end_points = List(Nested(VsbForwardingPathEndPointSerializer))

    @pre_load
    def is_valid(self, data, **kwargs):
        if len(data.get('hop_end_points', [])) == 0:
            raise ValidationError("VSB Forwarding Path hop without any end point")
        return data


class VsbEndpointSerializer(Schema):
    end_point_id = String(required=True, error_messages={"required": "VSB end point without ID"})
    external = Boolean()
    management = Boolean()
    ran_connection = Boolean()


class VsbLinkSerializer(Schema):
    end_point_ids = List(String())
    external = Boolean()
    name = String()
    connectivity_properties = List(String())


class ApplicationMetricSerializer(Schema):
    topic = String()
    metric_id = String()
    name = String()
    metric_collection_type = String(validate=validate.OneOf(MetricCollectionType.get_values()))
    unit = String()
    interval = String()

    @pre_load
    def is_valid(self, data, **kwargs):
        if data.get('topic', "") == "":
            raise ValidationError("Application metric without topic", "topic")

        elif data.get('metVsbActionsSerializerric_id', "") == "":
            raise ValidationError("Metric without metricId", "metric_id")

        elif data.get('name', "") == "":
            raise ValidationError("Metric without name", "name")

        elif data.get('unit', "") == "":
            raise ValidationError("Metric without unit", "unit")

        elif data.get('metric_collection_type', ""):
            raise ValidationError("Metric without MetricCollectionType", "metric_collection_type")

        return data


class VsBlueprintSerializer(Schema):
    blueprint_id = String()
    version = String(required=True, error_messages={"required": "VS blueprint without version"})
    name = String(required=True, error_messages={"required": "VS blueprint without name"})
    description = String()
    parameters = List(Nested(VsBlueprintParameterSerializer))
    atomic_components = List(Nested(VsComponentSerializer))
    service_sequence = List(Nested(VsbForwardingPathHopSerializer))
    end_points = List(Nested(VsbEndpointSerializer))
    connectivity_services = List(Nested(VsbLinkSerializer))
    configurable_parameters = List(String())
    application_metrics = List(Nested(ApplicationMetricSerializer))
    inter_site = Boolean()
    slice_service_type = String(validate=validate.OneOf(SliceServiceType.get_values()))
    embb_service_category = String(validate=validate.OneOf(EMBBServiceCategory.get_values()))
    urllc_service_category = String(validate=validate.OneOf(URLLCServiceCategory.get_values()))
    translation_rules = List(Nested(VsdNsdTranslationRuleSerializer))

    @pre_load
    def is_valid(self, data, **kwargs):
        if data.get('slice_service_type') == SliceServiceType.EMBB.value and data.get('embb_service_category') is None:
            raise ValidationError("VSB without slice service category", "slice_service_type & embb_service_category")

        elif data.get('slice_service_type') == SliceServiceType.URLLC.value and \
                data.get('urllc_service_category') is None:
            raise ValidationError("VSB without slice service category", "slice_service_type & urllc_service_category")

        return data


class VsBlueprintInfoSerializer(Schema):
    vs_blueprint = Nested(VsBlueprintSerializer)
    vs_blueprint_id = String(required=True, error_messages={"required": "VS Blueprint info without VS ID"})
    vs_blueprint_version = String(required=True, error_messages={"required": "VS Blueprint info without VS version"})
    name = String(required=True, error_messages={"required": "VS Blueprint info without VS name"})
    owner = String()
    on_boarded_nsd_info_id = List(String())
    on_boarded_nst_info_id = List(String())
    on_boarded_vnf_package_info_id = List(String())
    on_boarded_mec_app_package_info_id = List(String())
    active_vsd_id = List(String())
