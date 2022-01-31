from api.enums.utils import AutoName
from enum import auto


class TransportProtocolType(AutoName):
    REST_HTTP = auto()
    MB_TOPIC_BASED = auto()
    MB_ROUTING = auto()
    MB_PUBSUB = auto()
    RPC = auto()
    RPC_STREAMING = auto()
    WEBSOCKET = auto()


class OAuth20GrantType(AutoName):
    OAUTH2_AUTHORIZATION_CODE = auto()
    OAUTH2_IMPLICIT_GRANT = auto()
    OAUTH2_RESOURCE_OWNER = auto()
    OAUTH2_CLIENT_CREDENTIALS = auto()


class SerializerType(AutoName):
    JSON = auto()
    XML = auto()
    PROTOBUF3 = auto()


class TrafficFilterType(AutoName):
    FLOW = auto()
    PACKET = auto()


class MeHostPacketAction(AutoName):
    DROP = auto()
    FORWARD = auto()
    DECAPSULATED = auto()
    FORWARD_AS_IS = auto()
    PASSTHROUGH = auto()
    DUPLICATED_DECAPSULATED = auto()
    DUPLICATE_AS_IS = auto()


class NetworkInterfaceType(AutoName):
    TUNNEL = auto()
    MAC = auto()
    IP = auto()


class TunnelType(AutoName):
    GTP_U = auto()
    GRE = auto()


class VnfIndicatorSource(AutoName):
    VNF = auto()
    EM = auto()
    BOTH_VNF_EM = auto()
