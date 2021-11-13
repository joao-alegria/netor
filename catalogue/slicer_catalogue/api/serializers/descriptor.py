from marshmallow import Schema, pre_load, ValidationError, validate
from marshmallow.fields import String, Dict, Url, Nested, List, Date, Integer, Boolean

from api.enums.descriptor import LayerProtocol, CpRole, AddressType, IpVersion, ServiceAvailabilityLevel, AffinityType, \
    AffinityScope, LcmEventType


class AddressDataSerializer(Schema):
    address_type = String(validate=validate.OneOf(AddressType.get_values()))
    ip_address_assignment = Boolean()
    floating_ip_activated = Boolean()
    management = Boolean()
    ip_address_type = String(validate=validate.OneOf(IpVersion.get_values()))
    number_of_ip_address = Integer()


class CpdSerializer(Schema):
    cpd_id = String(required=True, error_messages={"required": "CPD without I"})
    layer_protocol = String(validate=validate.OneOf(LayerProtocol.get_values()), required=True,
                            error_messages={"required": "CPD without layer protocol"})
    cp_role = String(validate=validate.OneOf(CpRole.get_values()))
    description = String()
    address_data = List(Nested(AddressDataSerializer))


class VirtualNetworkInterfaceRequirementsSerializer(Schema):
    name = String()
    description = String()
    support_mandatory = Boolean()
    net_requirement = String(required=True,
                             error_messages={"required": "Virtual network interface requirement without requirement"})
    nic_io_requirements = String()


class SwImageDescSerializer(Schema):
    sw_image_id = String(required=True, error_messages={"required": "Sw Image Descriptor without ID"})
    name = String(required=True, error_messages={"required": "Sw Image Descriptor without name"})
    version = String(required=True, error_messages={"required": "Sw Image Descriptor without version"})
    checksum = String(required=True, error_messages={"required": "Sw Image Descriptor without checksum"})
    container_format = String()
    disk_format = String()
    min_disk = Integer()
    min_ram = Integer()
    size = Integer()
    sw_image = String(required=True, error_messages={"required": "Sw Image Descriptor without sw image"})
    operating_system = String()
    supported_virtualization_environment = String()


class MonitoringParameterSerializer(Schema):
    monitoring_parameter_id = String(required=True, error_messages={"required": "Monitoring Parameter without ID"})
    name = String()
    performance_metric = String(required=True, error_messages={"required": "Monitoring Parameter without metric"})
    exporter = String()
    params = Dict(keys=String(), values=String())
    type = String()


class VirtualMemoryDataSerializer(Schema):
    virtual_mem_size = Integer()
    virtual_mem_oversubscription_policy = String()
    numa_enabled = Boolean()


class VirtualCpuDataSerializer(Schema):
    cpu_architecture = String()
    num_virtual_cpu = Integer()
    virtual_cpu_clock = Integer()
    virtual_cpu_oversubscription_policy = String()


class RequestedAdditionalCapabilityDataSerializer(Schema):
    name = String(required=True, error_messages={"required": "Requested Additional Capability without name"})
    mandatory = Boolean()
    min_version = String()
    preferred_version = String()
    target_parameter = String()


class VirtualComputeDescSerializer(Schema):
    virtual_compute_desc_id = String(required=True,
                                     error_messages={"required": "Virtual compute descriptor without ID"})
    complexity_factor = String()
    logical_node = Dict(keys=String(), values=String())
    request_additional_capabilities = List(Nested(RequestedAdditionalCapabilityDataSerializer))
    virtual_memory = Nested(VirtualMemoryDataSerializer, required=True,
                            error_messages={"required": "Virtual compute descriptor without virtual memory data"})
    virtual_cpu = Nested(VirtualCpuDataSerializer, required=True,
                         error_messages={"required": "Virtual compute descriptor without vCPU data"})


class VirtualStorageDescSerializer(Schema):
    storage_id = String(required=True, error_messages={"required": "Virtual storage descriptor without id"})
    type_of_storage = String(required=True, error_messages={"required": "Virtual storage descriptor without type"})
    size_of_storage = Integer()
    rdma_enabled = Boolean()
    sw_image_desc = String()


class ConnectivityTypeSerializer(Schema):
    layer_protocol = String(validate=validate.OneOf(LayerProtocol.get_values()))
    flow_pattern = String()


class QoSSerializer(Schema):
    latency = Integer()
    packet_delay_variation = Integer()
    packet_loss_ratio = Integer()
    priority = Integer()


class VirtualLinkDfSerializer(Schema):
    flavour_id = String(required=True, error_messages={"required": "VL DF without flavour ID"})
    qos = Nested(QoSSerializer)
    service_availability_level = String(validate=validate.OneOf(ServiceAvailabilityLevel.get_values()))


class AffinityRuleSerializer(Schema):
    affinity_type = String(validate=validate.OneOf(AffinityType.get_values()))
    affinity_scope = String(validate=validate.OneOf(AffinityScope.get_values()))


class LinkBitrateRequirementsSerializer(Schema):
    root = String()
    leaf = String()


class VirtualLinkProfileSerializer(Schema):
    virtual_link_profile_id = String(required=True, error_messages={"required": "VL profile without ID"})
    virtual_link_desc_id = String(required=True, error_messages={"required": "VL profile without VLD ID"})
    flavour_id = String(required=True, error_messages={"required": "VL profile without VL flavour ID"})
    local_affinity_or_anti_affinity_rule = List(Nested(AffinityRuleSerializer))
    affinity_or_anti_affinity_group_id = List(String())
    max_bitrate_requirements = Nested(LinkBitrateRequirementsSerializer, required=True,
                                      error_messages={"required": "VL profile without max bitrate requirements"})
    min_bitrate_requirements = Nested(LinkBitrateRequirementsSerializer, required=True,
                                      error_messages={"required": "VL profile without min bitrate requirements"})


class ScaleInfoSerializer(Schema):
    aspect_id = String(required=True, error_messages={"required": "Scale info without aspect ID"})
    scale_level = Integer()


class TerminateVnfOpConfigSerializer(Schema):
    min_graceful_stop_timeout = String(required=True, error_messages={
        "required": "Operate VNF config data without minimum graceful stop timeout"})
    max_recommended_graceful_stop_timeout = String()


class AffinityOrAntiAffinityGroupSerializer(Schema):
    group_id = String(required=True, error_messages={"required": "Affinity group without ID"})
    affinity_type = String(validate=validate.OneOf(AffinityType.get_values()))
    affinity_scope = String(validate=validate.OneOf(AffinityScope.get_values()))


class LifeCycleManagementScriptSerializer(Schema):
    event = List(String(validate=validate.OneOf(LcmEventType.get_values())))
    script = String(required=True, error_messages={"required": "LCM script without script info"})

    @pre_load
    def is_valid(self, data, **kwargs):
        # print(data)
        if len(data.get('event', [])) == 0:
            raise ValidationError("LCM script without event", "event")

        return data
