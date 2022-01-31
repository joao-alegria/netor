from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, ListField, EnumField, BooleanField, IntField, EmbeddedDocumentField, \
    MapField, EmbeddedDocumentListField
from api.enums.ns_descriptor import NsScaleType, ScalingProcedureType, LogicOperation, RelationalOperation
from api.enums.descriptor import LayerProtocol, CpRole, AddressType, IpVersion, ServiceAvailabilityLevel, LcmEventType, \
    AffinityType, AffinityScope


class AddressData(EmbeddedDocument):
    address_type = EnumField(AddressType)
    ip_address_assignment = BooleanField()
    floating_ip_activated = BooleanField()
    management = BooleanField()
    ip_address_type = EnumField(IpVersion)
    number_of_ip_address = IntField()


class Sapd(EmbeddedDocument):
    cpi_id = StringField()
    layer_protocol = EnumField(LayerProtocol)
    cp_role = EnumField(CpRole)
    description = StringField()
    address_data = EmbeddedDocumentListField(AddressData)
    sap_address_assignment = BooleanField()
    ns_virtual_link_desc_id = StringField()
    associated_cdp_id = StringField()


class ConnectivityType(EmbeddedDocument):
    layer_protocol = EnumField(LayerProtocol)
    flow_pattern = StringField()


class QoS(EmbeddedDocument):
    latency = IntField()
    packet_delay_variation = IntField()
    packet_loss_ratio = IntField()
    priority = IntField()


class VirtualLinkDf(EmbeddedDocument):
    flavour_id = StringField()
    qos = EmbeddedDocumentField(QoS)
    service_availability_level = EnumField(ServiceAvailabilityLevel)


class SecurityParameters(EmbeddedDocument):
    signature = StringField()
    algorithm = StringField()
    certificate = StringField()


class NsVirtualLinkDesc(EmbeddedDocument):
    virtual_link_desc_id = StringField()
    virtual_link_desc_provider = StringField()
    virtual_link_desc_version = StringField()
    connectivity_type = EmbeddedDocumentField(ConnectivityType)
    virtual_link_df = EmbeddedDocumentListField(VirtualLinkDf)
    test_access = ListField(StringField())
    description = StringField()
    security = EmbeddedDocumentField(SecurityParameters)


class Nfpd(EmbeddedDocument):
    nfp_id = StringField()
    # nfp_rule =
    cpd = ListField(StringField())
    qos = EmbeddedDocumentField(QoS)


class Vnffgd(EmbeddedDocument):
    vnffgd_id = StringField()
    vnfd_id = ListField(StringField())
    pnfd_id = ListField(StringField())
    virtual_link_desc_id = ListField(StringField())
    cpd_pool_id = ListField(StringField())
    nfpd = EmbeddedDocumentListField(Nfpd)


class VnfIndicatorData(EmbeddedDocument):
    vnfd_id = StringField()
    vnf_indicator = StringField()


class MonitoringParameter(EmbeddedDocument):
    monitoring_parameter_id = StringField()
    name = StringField()
    performance_metric = StringField()
    exporter = StringField()
    params = MapField(StringField())
    type = StringField()


class MonitoredData(EmbeddedDocument):
    vnf_indicator_info = EmbeddedDocumentField(VnfIndicatorData)
    monitoring_parameter = EmbeddedDocumentField(MonitoringParameter)


class NsScaleInfo(EmbeddedDocument):
    ns_scaling_aspect_id = StringField()
    ns_scale_level_Id = StringField()


class ScaleNsToLevelData(EmbeddedDocument):
    ns_instantiation_level = StringField()
    ns_scale_info = EmbeddedDocumentListField(NsScaleInfo)


class AutoscalingAction(EmbeddedDocument):
    scale_type = EnumField(NsScaleType)
    scale_ns_to_level_data = EmbeddedDocumentField(ScaleNsToLevelData)


class AutoscalingRuleCriteria(EmbeddedDocument):
    name = StringField()
    scale_in_threshold = IntField()
    scale_in_relational_operation = EnumField(RelationalOperation)
    scale_out_threshold = IntField()
    scale_out_relational_operation = EnumField(RelationalOperation)
    ns_monitoring_param_ref = StringField()


class AutoscalingRuleCondition(EmbeddedDocument):
    name = StringField()
    scaling_type = EnumField(ScalingProcedureType)
    enabled = BooleanField()
    scale_in_operation_type = EnumField(LogicOperation)
    scale_out_operation_type = EnumField(LogicOperation)
    threshold_time = IntField()
    cooldown_time = IntField()
    initial_instantiation_level = StringField()
    scaling_criteria = EmbeddedDocumentListField(AutoscalingRuleCriteria)


class NsAutoscalingRule(EmbeddedDocument):
    rule_id = StringField()
    rule_condition = EmbeddedDocumentField(AutoscalingRuleCondition)
    rule_actions = EmbeddedDocumentListField(AutoscalingAction)


class LifeCycleManagementScript(EmbeddedDocument):
    event = ListField(EnumField(LcmEventType))
    script = StringField()


class AffinityRule(EmbeddedDocument):
    affinity_type = EnumField(AffinityType)
    affinity_scope = EnumField(AffinityScope)


class NsVirtualLinkConnectivity(EmbeddedDocument):
    virtual_link_profile_id = StringField()
    cpd_id = ListField(StringField())


class VnfConfigurationScript(EmbeddedDocument):
    args = MapField(StringField())
    script = ListField(StringField())


class VnfLCMScripts(EmbeddedDocument):
    target = StringField()
    scripts = MapField(EmbeddedDocumentField(VnfConfigurationScript))


class VnfProfile(EmbeddedDocument):
    vnf_profile_id = StringField()
    vnfd_id = StringField()
    flavour_id = StringField()
    instantiation_level = StringField()
    min_number_of_instances = IntField()
    max_number_of_instances = IntField()
    local_affinity_or_anti_affinity_rule = EmbeddedDocumentListField(AffinityRule)
    affinity_or_anti_affinity_group_id = ListField(StringField())
    ns_virtual_link_connectivity = EmbeddedDocumentListField(NsVirtualLinkConnectivity)
    script = EmbeddedDocumentListField(VnfLCMScripts)


class PnfProfile(EmbeddedDocument):
    pnf_profile_id = StringField()
    pnfd_id = StringField()
    ns_virtual_link_connectivity = EmbeddedDocumentListField(NsVirtualLinkConnectivity)


class LinkBitrateRequirements(EmbeddedDocument):
    root = StringField()
    leaf = StringField()


class VirtualLinkProfile(EmbeddedDocument):
    virtual_link_profile_id = StringField()
    virtual_link_desc_id = StringField()
    flavour_id = StringField()
    local_affinity_or_anti_affinity_rule = EmbeddedDocumentListField(AffinityRule)
    affinity_or_anti_affinity_group_id = ListField(StringField())
    max_bitrate_requirements = EmbeddedDocumentField(LinkBitrateRequirements)
    min_bitrate_requirements = EmbeddedDocumentField(LinkBitrateRequirements)


class VnfToLevelMapping(EmbeddedDocument):
    vnf_profile_id = StringField()
    number_of_instances = IntField()


class NsToLevelMapping(EmbeddedDocument):
    ns_profile_id = StringField()
    number_of_instances = IntField()


class VirtualLinkToLevelMapping(EmbeddedDocument):
    virtual_link_profile_id = StringField()
    bit_rate_requirements = EmbeddedDocumentField(LinkBitrateRequirements)


class NsLevel(EmbeddedDocument):
    ns_level_id = StringField()
    description = StringField()
    vnf_to_level_mapping = EmbeddedDocumentListField(VnfToLevelMapping)
    ns_to_level_mapping = EmbeddedDocumentListField(NsToLevelMapping)
    virtual_link_to_level_mapping = EmbeddedDocumentListField(VirtualLinkToLevelMapping)


class NsScalingAspect(EmbeddedDocument):
    ns_scaling_aspect_id = StringField()
    name = StringField()
    description = StringField()
    ns_scale_level = EmbeddedDocumentListField(NsLevel)


class AffinityOrAntiAffinityGroup(EmbeddedDocument):
    group_id = StringField()
    affinity_type = EnumField(AffinityType)
    affinity_scope = EnumField(AffinityScope)


class NsProfile(EmbeddedDocument):
    ns_profile_id = StringField()
    nsd_id = StringField()
    ns_deployment_flavour_id = StringField()
    ns_instantiation_level_id = StringField()
    min_number_of_instances = IntField()
    max_number_of_instances = IntField()
    affinity_or_anti_affinity_group_id = ListField(StringField())
    ns_virtual_link_connectivity = EmbeddedDocumentListField(NsVirtualLinkConnectivity)


class Dependencies(EmbeddedDocument):
    primary_id = ListField(StringField())
    secondary_id = ListField(StringField())


class NsDf(EmbeddedDocument):
    ns_df_id = StringField()
    flavour_key = StringField()
    vnf_profile = EmbeddedDocumentListField(VnfProfile)
    pnf_profile = EmbeddedDocumentListField(PnfProfile)
    virtual_link_profile = EmbeddedDocumentListField(VirtualLinkProfile)
    scaling_aspect = EmbeddedDocumentListField(NsScalingAspect)
    affinity_or_anti_affinity_group = EmbeddedDocumentListField(AffinityOrAntiAffinityGroup)
    ns_instantiation_level = EmbeddedDocumentListField(NsLevel)
    default_ns_instantiation_level_id = StringField()
    ns_profile = EmbeddedDocumentListField(NsProfile)
    dependencies = EmbeddedDocumentListField(Dependencies)


class Nsd(Document):
    nsd_identifier = StringField()
    designer = StringField()
    version = StringField()
    nsd_name = StringField()
    nsd_invariant_id = StringField()
    nested_id = ListField(StringField())
    vnfd_id = ListField(StringField())
    pnfd_id = ListField(StringField())
    sapd = EmbeddedDocumentListField(Sapd)
    virtual_link_desc = EmbeddedDocumentListField(NsVirtualLinkDesc)
    vnffgd = EmbeddedDocumentListField(Vnffgd)
    monitored_info = EmbeddedDocumentListField(MonitoredData)
    auto_scaling_rule = EmbeddedDocumentListField(NsAutoscalingRule)
    life_cycle_management_script = EmbeddedDocumentListField(LifeCycleManagementScript)
    ns_df = EmbeddedDocumentListField(NsDf)
    security = EmbeddedDocumentField(SecurityParameters)

    @classmethod
    def get_collection(cls):
        return cls._get_collection()
