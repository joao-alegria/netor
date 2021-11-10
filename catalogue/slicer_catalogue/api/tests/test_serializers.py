"""
Test serializers' validators
"""
from api.enums.vs_blueprint import VsComponentType, SliceServiceType
from api.tests.utils import catch_exception, error_catcher, mixer
from api.serializers.requests import VsBlueprintRequestSerializer
from api.serializers.vs_blueprint import VsdNsdTranslationRuleSerializer, VsdParameterValueRangeSerializer, \
    VsBlueprintParameterSerializer, VsBlueprintSerializer, VsComponentSerializer, VsbForwardingPathEndPointSerializer, \
    VsbEndpointSerializer
from api.serializers.vnf import OnBoardVnfPackageRequestSerializer
from api.serializers.vs_descriptor import VsDescriptorSerializer


def generate_data(cls, remove_fields=None):
    if remove_fields is None:
        remove_fields = []

    data = {}

    for i in range(100):
        data = mixer.blend(cls)
        if data is not None:
            break

    for field in remove_fields:
        data.pop(field, None)

    return data


# VsdParameterValueRangeSerializer
@catch_exception
def test_vsd_parameter_value_range_serializer_invalid_parameter_id(error_catcher):
    field = "parameter_id"
    data = generate_data(VsdParameterValueRangeSerializer, remove_fields=[field])
    errors = VsdParameterValueRangeSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VSD parameter value range without ID."


# VsdNsdTranslationRuleSerializer
@catch_exception
def test_vsd_nsd_translation_rule_serializer_invalid_input_none(error_catcher):
    field = "input"
    data = generate_data(VsdNsdTranslationRuleSerializer, remove_fields=[field])
    errors = VsdNsdTranslationRuleSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VSD NSD translation rule without matching conditions"


@catch_exception
def test_vsd_nsd_translation_rule_serializer_invalid_input_empty(error_catcher):
    field = "input"
    data = generate_data(VsdNsdTranslationRuleSerializer)
    data[field] = []
    errors = VsdNsdTranslationRuleSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VSD NSD translation rule without matching conditions"


@catch_exception
def test_vsd_nsd_translation_rule_serializer_invalid_nst_id_and_nsd_id(error_catcher):
    fields = ["nst_id", "nsd_id"]
    data = generate_data(VsdNsdTranslationRuleSerializer, remove_fields=fields)
    errors = VsdNsdTranslationRuleSerializer().validate(data)
    assert len(errors) > 0 and errors.get(" & ".join(fields))[0] == "VSD NSD translation rule without NSD ID/NST ID"


@catch_exception
def test_vsd_nsd_translation_rule_serializer_invalid_nsd_id_and_nsd_version(error_catcher):
    field = "nsd_version"
    data = generate_data(VsdNsdTranslationRuleSerializer, remove_fields=[field])
    errors = VsdNsdTranslationRuleSerializer().validate(data)
    assert len(errors) > 0 and errors.get(f'nsd_id & {field}')[0] == "VSD NSD translation rule without NSD version"


# OnBoardVnfPackageRequestSerializer
@catch_exception
def test_on_board_vnf_package_request_serializer_invalid_name(error_catcher):
    field = "name"
    data = generate_data(OnBoardVnfPackageRequestSerializer, remove_fields=[field])
    errors = OnBoardVnfPackageRequestSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "On board VNF package request without name"


@catch_exception
def test_on_board_vnf_package_request_serializer_invalid_version(error_catcher):
    field = "version"
    data = generate_data(OnBoardVnfPackageRequestSerializer, remove_fields=[field])
    errors = OnBoardVnfPackageRequestSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "On board VNF package request without version"


@catch_exception
def test_on_board_vnf_package_request_serializer_invalid_version(error_catcher):
    field = "provider"
    data = generate_data(OnBoardVnfPackageRequestSerializer, remove_fields=[field])
    errors = OnBoardVnfPackageRequestSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "On board VNF package request without provider"


@catch_exception
def test_on_board_vnf_package_request_serializer_invalid_version(error_catcher):
    field = "checksum"
    data = generate_data(OnBoardVnfPackageRequestSerializer, remove_fields=[field])
    errors = OnBoardVnfPackageRequestSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "On board VNF package request without checksum"


@catch_exception
def test_on_board_vnf_package_request_serializer_invalid_version(error_catcher):
    field = "vnf_package_path"
    data = generate_data(OnBoardVnfPackageRequestSerializer, remove_fields=[field])
    errors = OnBoardVnfPackageRequestSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "On board VNF package request without package path"


# VsBlueprintRequestSerializer
@catch_exception
def test_vs_blueprint_request_serializer_invalid_vs_blueprint(error_catcher):
    field = "vs_blueprint"
    data = generate_data(VsBlueprintRequestSerializer, remove_fields=[field])
    errors = VsBlueprintRequestSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "Onboard VS blueprint request without VS blueprint"


# VsBlueprintParameterSerializer
@catch_exception
def test_vs_blueprint_parameter_serializer_invalid_parameter_id(error_catcher):
    field = "parameter_id"
    data = generate_data(VsBlueprintParameterSerializer, remove_fields=[field])
    errors = VsBlueprintParameterSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VS blueprint parameter without ID"


# VsComponentSerializer
@catch_exception
def test_vs_component_serializer_invalid_component_id(error_catcher):
    field = "component_id"
    data = generate_data(VsComponentSerializer, remove_fields=[field])
    errors = VsComponentSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VSB atomic component without ID."


@catch_exception
def test_vs_component_serializer_invalid_type_and_associated_vsb_id(error_catcher):
    field = "associated_vsb_id"
    data = generate_data(VsComponentSerializer, remove_fields=[field])
    data['type'] = VsComponentType.SERVICE.value
    errors = VsComponentSerializer().validate(data)
    assert len(errors) > 0 and errors.get(f'type & {field}')[0] == "Component of type service without associated VSB id"


# VsbForwardingPathEndPointSerializer
@catch_exception
def test_vsb_forwarding_path_end_point_serializer_invalid_vs_component_id(error_catcher):
    field = "vs_component_id"
    data = generate_data(VsbForwardingPathEndPointSerializer, remove_fields=[field])
    errors = VsbForwardingPathEndPointSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VS Forwarding Graph element without VS component"


@catch_exception
def test_vsb_forwarding_path_end_point_serializer_invalid_vs_component_id(error_catcher):
    field = "end_point_id"
    data = generate_data(VsbForwardingPathEndPointSerializer, remove_fields=[field])
    errors = VsbForwardingPathEndPointSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VS Forwarding Graph element without end point"


# VsbEndpointSerializer
@catch_exception
def test_vsb_endpoint_serializer_invalid_end_point_id(error_catcher):
    field = "end_point_id"
    data = generate_data(VsbEndpointSerializer, remove_fields=[field])
    errors = VsbEndpointSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VSB end point without ID"


# VsBlueprintSerializer
@catch_exception
def test_vs_blueprint_serializer_invalid_version(error_catcher):
    field = "version"
    data = generate_data(VsBlueprintSerializer, remove_fields=[field])
    errors = VsBlueprintSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VS blueprint without version"


@catch_exception
def test_vs_blueprint_serializer_invalid_version(error_catcher):
    field = "name"
    data = generate_data(VsBlueprintSerializer, remove_fields=[field])
    errors = VsBlueprintSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VS blueprint without name"


@catch_exception
def test_vs_blueprint_serializer_invalid_slice_service_type_and_embb_service_category(error_catcher):
    field = "embb_service_category"
    data = generate_data(VsBlueprintSerializer, remove_fields=[field])
    data['slice_service_type'] = SliceServiceType.EMBB.value
    errors = VsBlueprintSerializer().validate(data)
    assert len(errors) > 0 and errors.get(f"slice_service_type & {field}")[0] == "VSB without slice service category"


@catch_exception
def test_vs_blueprint_serializer_invalid_slice_service_type_and_embb_urllc_service_category(error_catcher):
    field = "urllc_service_category"
    data = generate_data(VsBlueprintSerializer, remove_fields=[field])
    data['slice_service_type'] = SliceServiceType.URLLC.value
    errors = VsBlueprintSerializer().validate(data)
    assert len(errors) > 0 and errors.get(f"slice_service_type & {field}")[0] == "VSB without slice service category"


# VsDescriptorSerializer
@catch_exception
def test_vs_descriptor_invalid_name(error_catcher):
    field = "name"
    data = generate_data(VsDescriptorSerializer, remove_fields=[field])
    errors = VsDescriptorSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VSD without name"


@catch_exception
def test_vs_descriptor_invalid_version(error_catcher):
    field = "version"
    data = generate_data(VsDescriptorSerializer, remove_fields=[field])
    errors = VsDescriptorSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VSD without version"


@catch_exception
def test_vs_descriptor_invalid_vs_blueprint_id(error_catcher):
    field = "vs_blueprint_id"
    data = generate_data(VsDescriptorSerializer, remove_fields=[field])
    errors = VsDescriptorSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VSD without VS blueprint ID"
