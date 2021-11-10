from marshmallow import Schema, validate
from marshmallow.fields import String, List, Boolean, Integer, Nested, Float
from api.enums.ns_template import UEMobilityLevel, SliceType, NsstType


class GeographicalAreaInfoSerializer(Schema):
    LAT_MAX_DISTANCE = 0.005
    LON_MAX_DISTANCE = 0.01
    description = String()
    lat = Float()
    lon = Float()
    used = Float()


class EMBBPerfReqSerializer(Schema):
    exp_data_rate_DL = Integer()
    exp_data_rate_uL = Integer()
    area_traffic_cap_DL = Integer()
    area_traffic_cap_UL = Integer()
    user_density = Integer()
    activity_factor = Integer()
    uE_speed = Integer()
    coverage = String()


class URLLCPerfReqSerializer(Schema):
    e2e_latency = Integer()
    jitter = Integer()
    survival_time = Integer()
    cS_availability = Float()
    reliability = Float()
    exp_data_rate = Integer()
    payload_size = String()
    traffic_density = Integer()
    conn_density = Integer()
    service_area_dimension = String()


class NstServiceProfileSerializer(Schema):
    service_profile_id = String()
    pLMN_id_list = List(String())
    eMBB_perf_req = List(Nested(EMBBPerfReqSerializer))
    uRLLC_perf_req = List(Nested(URLLCPerfReqSerializer))
    max_number_of_UEs = Integer()
    coverage_area_TA_list = List(String())
    latency = Integer()
    uE_mobility_level = String(validate=validate.OneOf(UEMobilityLevel.get_values()))
    resource_sharing_level = Boolean()
    sST = String(validate=validate.OneOf(SliceType.get_values()))
    availability = Float()


class NstSerializer(Schema):
    nst_id = String(required=True, error_messages={"required": "NST id not set"})
    nst_name = String()
    nst_version = String(required=True, error_messages={"required": "NST version not set"})
    nst_provider = String(required=True, error_messages={"required": "NST provider not set"})
    geographical_area_info_list = List(Nested(GeographicalAreaInfoSerializer))
    nsst_ids = List(String())
    nsst = List(Nested('self'))
    nsd_id = String()
    nsd_version = String()
    nst_service_profile = Nested(NstServiceProfileSerializer)
    nsst_type = String(validate=validate.OneOf(NsstType.get_values()))
