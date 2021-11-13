from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, ListField, BooleanField, IntField, EmbeddedDocumentField, \
    EmbeddedDocumentListField, FloatField, ReferenceField

from api.enums.ns_template import UEMobilityLevel, SliceType, NsstType
from api.queries.utils import get_or_error


class GeographicalAreaInfo(EmbeddedDocument):
    LAT_MAX_DISTANCE = 0.005
    LON_MAX_DISTANCE = 0.01
    description = StringField()
    lat = FloatField()
    lon = FloatField()
    used = BooleanField()


class EMBBPerfReq(EmbeddedDocument):
    exp_data_rate_DL = IntField()
    exp_data_rate_uL = IntField()
    area_traffic_cap_DL = IntField()
    area_traffic_cap_UL = IntField()
    user_density = IntField()
    activity_factor = IntField()
    uE_speed = IntField()
    coverage = StringField()


class URLLCPerfReq(EmbeddedDocument):
    e2e_latency = IntField()
    jitter = IntField()
    survival_time = IntField()
    cS_availability = FloatField()
    reliability = FloatField()
    exp_data_rate = IntField()
    payload_size = StringField()
    traffic_density = IntField()
    conn_density = IntField()
    service_area_dimension = StringField()


class NstServiceProfile(EmbeddedDocument):
    service_profile_id = StringField()
    pLMN_id_list = ListField(StringField())
    eMBB_perf_req = EmbeddedDocumentListField(EMBBPerfReq)
    uRLLC_perf_req = EmbeddedDocumentListField(URLLCPerfReq)
    max_number_of_UEs = IntField()
    coverage_area_TA_list = ListField(StringField())
    latency = IntField()
    uE_mobility_level = StringField(choices=UEMobilityLevel.get_values())
    resource_sharing_level = BooleanField()
    sST = StringField(choices=SliceType.get_values())
    availability = FloatField()


class Nst(Document):
    nst_id = StringField()
    nst_name = StringField()
    nst_version = StringField()
    nst_provider = StringField()
    geographical_area_info_list = EmbeddedDocumentListField(GeographicalAreaInfo)
    nsst_ids = ListField(StringField())
    nsst = ListField(ReferenceField('self'))
    nsd_id = StringField()
    nsd_version = StringField()
    nst_service_profile = EmbeddedDocumentField(NstServiceProfile)
    nsst_type = StringField(choices=NsstType.get_values())

    @classmethod
    def get_or_404(cls, **kwargs):
        return get_or_error(cls, **kwargs)

    @classmethod
    def get_collection(cls):
        return cls._get_collection()