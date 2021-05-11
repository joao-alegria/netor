import pytest
import redisHandler
import rabbitmq.adaptor
import manager
import json

@pytest.fixture
def csmfMock(monkeypatch, redisSet, rabbit):
    def mock_polling(*args, **kwargs):
        return None
    monkeypatch.setattr(manager.Polling, "__init__", mock_polling)
    monkeypatch.setattr(manager.Polling, "start", mock_polling)

    csmf = manager.CSMF("1",{})
    csmf.start()

    rabbitmq.adaptor.Messaging.publish2Queue.assert_called_with('vsCoordinator', '{"msgType": "statusUpdate", "data": {"vsiId": "1", "status": "creating", "message": "Created Management Function, waiting to receive all necessary information"}}')

    yield csmf
    csmf.stop()

@pytest.fixture
def rabbit(monkeypatch, mocker):
    def mock_messaging(*args, **kwargs):
        return None
    monkeypatch.setattr(rabbitmq.adaptor.Messaging, "__init__", mock_messaging)

    def mock_messagingConsume(*args, **kwargs):
        return None
    monkeypatch.setattr(rabbitmq.adaptor.Messaging, "consumeQueue", mock_messagingConsume)

    mocker.patch('rabbitmq.adaptor.Messaging.publish2Queue')
    mocker.patch('rabbitmq.adaptor.Messaging.publish2Exchange')

@pytest.fixture
def badRedis(monkeypatch):
    def mock_redisGetEntireHash(*args, **kwargs):
        return {
            "domainInfo".encode("UTF-8"):json.dumps({"vsiId":"1","error":False, "message":"TestDomain"}),
            "tenantInfo".encode("UTF-8"):json.dumps({"vsiId":"1","error":False, "message":"TestTenant"}),
            "catalogueInfo".encode("UTF-8"):json.dumps({"vsiId":"1","error":True, "message":"TestCatalogue"}),
            "placementInfo".encode("UTF-8"):json.dumps({"vsiId":"1","error":True, "message":"TestPlacement"}),
            "vsiRequest".encode("UTF-8"):json.dumps({"vsiId":"1","error":True, "message":"TestVSIRequest"})
            }
    monkeypatch.setattr(redisHandler, "getEntireHash", mock_redisGetEntireHash)

@pytest.fixture
def goodRedis(monkeypatch):
    def mock_redisGetEntireHash(*args, **kwargs):
        return {
            "vsiRequest".encode("UTF-8"):json.dumps({"msgType": "createVSI", "vsiId": "2", "tenantId": "user", "data": {"name": "test", "vsdId": "608ae08e063c52ff4d88f32f", "domainId": "ITAV", "vsiId": "2", "domainPlacements": [{"domainId": "DETI", "componentName": "test_VSI-1_1"}, {"domainId": "DETI", "componentName": "test_VSI-1_2"}]}}),
            "placementInfo".encode("UTF-8"):json.dumps({"vsiId": "2", "msgType": "placementInfo", "error": False, "message": "Success", "data": [{"domainId": "ITAV", "sliceEnabled": False, "nsdId": "interdomain_slice_nsd"}, {"domainId": "ITAV", "sliceEnabled": False, "nsdId": "interdomain_slice_nsd"}]}),
            "domainInfo".encode("UTF-8"):json.dumps({"vsiId":"2","error":False, "message":"TestDomain", "data":["ITAV"]}),
            "tenantInfo".encode("UTF-8"):json.dumps({"vsiId": "2", "msgType": "tenantInfo", "data": {"username": "user", "group": "user", "vcpu": 100, "slas": [], "memory": 100, "storage": 100, "role": "TENANT"}, "error": False}),
            "catalogueInfo".encode("UTF-8"):json.dumps({"message": "Success", "vsiId": "2", "msgType": "catalogueInfo", "error": False, "data": {"vsd": {"tenant_id": "user", "associated_vsd_id": None, "domain_id": "ITAV", "vs_descriptor_id": "608ae08e063c52ff4d88f32f", "version": "1.0", "is_public": True, "nested_vsd_ids": {}, "service_constraints": [], "vs_blueprint_id": "608ae069063c52ff4d88f327", "name": "vsdTest", "sla": None, "management_type": "TENANT_MANAGED", "qos_parameters": {"peers": "2"}}, "vs_blueprint_info": {"vs_blueprint": {"urllc_service_category": None, "end_points": [], "inter_site": True, "parameters": [{"parameter_id": "peers", "parameter_type": "number", "applicability_field": "interdomain", "parameter_name": "Peers", "parameter_description": "#Peers"}], "version": "version_1", "blueprint_id": "608ae069063c52ff4d88f327", "service_sequence": [], "translation_rules": [{"nsd_version": "1.0", "input": [{"parameter_id": "peers", "max_value": 5, "min_value": 1}], "nsd_id": "interdomain-ns", "nst_id": "interdomain_e2e_nst", "blueprint_id": "608ae069063c52ff4d88f327", "nsd_info_id": None, "ns_instantiation_level_id": None, "ns_flavour_id": None}], "name": "vsb-test", "description": None, "atomic_components": [], "configurable_parameters": [], "application_metrics": [], "connectivity_services": [], "embb_service_category": "URBAN_MACRO", "slice_service_type": "EMBB"}, "on_boarded_nst_info_id": [], "on_boarded_mec_app_package_info_id": [], "on_boarded_vnf_package_info_id": [], "owner": None, "active_vsd_id": ["VsDescriptor object"], "vs_blueprint_id": "608ae069063c52ff4d88f327", "name": "vsb-test", "vs_blueprint_version": "version_1", "on_boarded_nsd_info_id": []}, "nsts": [{"nst_name": "Interdomain Slice", "nsst": [{"nst_name": "Interdomain Slice Subnet", "nsst": [], "nsd_version": "1.0", "geographical_area_info_list": [], "nst_provider": "ITAV", "nsd_id": "interdomain_slice_nsd", "nst_id": "interdomain_nsst", "nst_version": "1.0", "nst_service_profile": {"latency": 100, "sST": "EMBB", "resource_sharing_level": None, "max_number_of_UEs": 1000, "coverage_area_TA_list": [], "service_profile_id": "interdomain_profile", "uRLLC_perf_req": [], "availability": 100.0, "pLMN_id_list": [], "eMBB_perf_req": [{"user_density": 100, "activity_factor": None, "exp_data_rate_DL": None, "area_traffic_cap_DL": None, "area_traffic_cap_UL": None, "uE_speed": 10, "coverage": None, "exp_data_rate_uL": None}], "uE_mobility_level": None}, "nsst_type": "NONE", "nsst_ids": []}, {"nst_name": "Interdomain Slice Subnet", "nsst": [], "nsd_version": "1.0", "geographical_area_info_list": [], "nst_provider": "ITAV", "nsd_id": "interdomain_slice_nsd", "nst_id": "interdomain_nsst", "nst_version": "1.0", "nst_service_profile": {"latency": 100, "sST": "EMBB", "resource_sharing_level": None, "max_number_of_UEs": 1000, "coverage_area_TA_list": [], "service_profile_id": "interdomain_profile", "uRLLC_perf_req": [], "availability": 100.0, "pLMN_id_list": [], "eMBB_perf_req": [{"user_density": 100, "activity_factor": None, "exp_data_rate_DL": None, "area_traffic_cap_DL": None, "area_traffic_cap_UL": None, "uE_speed": 10, "coverage": None, "exp_data_rate_uL": None}], "uE_mobility_level": None}, "nsst_type": "NONE", "nsst_ids": []}], "nsd_version": "1.0", "geographical_area_info_list": [], "nst_provider": "ITAV", "nsd_id": None, "nst_id": "interdomain_e2e_nst", "nst_version": "1.0", "nst_service_profile": {"latency": 100, "sST": "EMBB", "resource_sharing_level": None, "max_number_of_UEs": 1000, "coverage_area_TA_list": [], "service_profile_id": "interdomain_profile", "uRLLC_perf_req": [], "availability": 100.0, "pLMN_id_list": [], "eMBB_perf_req": [{"user_density": 100, "activity_factor": None, "exp_data_rate_DL": None, "area_traffic_cap_DL": None, "area_traffic_cap_UL": None, "uE_speed": 10, "coverage": None, "exp_data_rate_uL": None}], "uE_mobility_level": None}, "nsst_type": "NONE", "nsst_ids": ["interdomain_nsst", "interdomain_nsst"]}], "vsb_actions": [{"action_name": "Add Tunnel Peer", "action_id": "addpeer", "parameters": [{"parameter_type": "STRING", "parameter_id": "peer_network", "parameter_name": "Peer Network", "parameter_default_value": "10.0.0.0/24"}], "blueprint_id": "608ae069063c52ff4d88f327"}, {"action_name": "Fetch Tunnel Peer Info", "action_id": "getvnfinfo", "parameters": [], "blueprint_id": "608ae069063c52ff4d88f327"}]}})
            }
    monkeypatch.setattr(redisHandler, "getEntireHash", mock_redisGetEntireHash)


@pytest.fixture
def basicGetValue(monkeypatch):
    def mock_redisGetValue(*args, **kwargs):
        return json.dumps({})
    monkeypatch.setattr(redisHandler, "getHashValue", mock_redisGetValue)

@pytest.fixture
def interdomainRedis(monkeypatch):
    def mock_redisGetValue(channel, vsiId):
        if channel=="serviceComposition":
            return json.dumps({"vsiId_1":{"sliceEnabled":False,"domainId":"ITAV","nfvoId":"1111"}, "vsiId_2":{"sliceEnabled":False,"domainId":"ITAV", "nfvoId":"2222"}})
        elif channel=="interdomainInfo":
            return json.dumps({"vsiId_1":{"tunnelId":"vsiId_1","vnfIp":"1.1.1.1", "publicKey":"key1"}})
    monkeypatch.setattr(redisHandler, "getHashValue", mock_redisGetValue)

@pytest.fixture
def redisSet(monkeypatch):
    def mock_redisSetValue(*args, **kwargs):
        return 0
    monkeypatch.setattr(redisHandler, "setKeyValue", mock_redisSetValue)

def test_propagatesError(csmfMock,badRedis):
    csmfMock.instantiateVSI()
    rabbitmq.adaptor.Messaging.publish2Queue.assert_called_with('vsCoordinator', '{"msgType": "statusUpdate", "data": {"vsiId": "1", "status": "failed", "message": "\\nCatalogue error: TestCatalogue"}}')

def test_processesCorrectly(csmfMock,goodRedis, basicGetValue):
    csmfMock.instantiateVSI()
    rabbitmq.adaptor.Messaging.publish2Queue.assert_any_call('vsDomain', '{"msgType": "instantiateNs", "data": {"name": "test_VSI-1_1", "domainId": "ITAV", "nsdId": "interdomain_slice_nsd", "additionalConf": "additionalParamsForVnf:\\n- additionalParams:\\n    tunnel_address: 10.0.0.1/24\\n    tunnel_id: test_VSI-1_1\\n    vsi_id: \'1\'\\n  member-vnf-index: \'1\'\\n"}, "vsiId": "1"}')
    rabbitmq.adaptor.Messaging.publish2Queue.assert_any_call('vsDomain', '{"msgType": "instantiateNs", "data": {"name": "test_VSI-1_2", "domainId": "ITAV", "nsdId": "interdomain_slice_nsd", "additionalConf": "additionalParamsForVnf:\\n- additionalParams:\\n    tunnel_address: 10.0.0.2/24\\n    tunnel_id: test_VSI-1_2\\n    vsi_id: \'1\'\\n  member-vnf-index: \'1\'\\n"}, "vsiId": "1"}')
    rabbitmq.adaptor.Messaging.publish2Queue.assert_any_call('vsCoordinator', '{"msgType": "statusUpdate", "data": {"vsiId": "1", "status": "deploying", "message": "Sent all instantiation requests to the appropriate domains"}}')

def test_interdomainHandler(csmfMock,interdomainRedis, goodRedis):
    csmfMock.interdomainHandler({"tunnelId":"vsiId_1","vnfIp":"1.1.1.1", "publicKey":"key1", "domainId":"ITAV"})
    csmfMock.interdomainHandler({"tunnelId":"vsiId_2","vnfIp":"2.2.2.2", "publicKey":"key2", "domainId":"ITAV"})
    rabbitmq.adaptor.Messaging.publish2Queue.assert_any_call('vsDomain', '{"msgType": "actionNs", "data": {"primitiveName": "addpeer", "domainId": "ITAV", "nsId": "2222", "additionalConf": {"member_vnf_index": "1", "primitive": "addpeer", "primitive_params": {"peer_endpoint": "1.1.1.1", "peer_key": "key1", "peer_network": "10.0.0.0/24"}}}}')
    rabbitmq.adaptor.Messaging.publish2Queue.assert_any_call('vsDomain', '{"msgType": "actionNs", "data": {"primitiveName": "addpeer", "domainId": "ITAV", "nsId": "1111", "additionalConf": {"member_vnf_index": "1", "primitive": "addpeer", "primitive_params": {"peer_endpoint": "2.2.2.2", "peer_key": "key2", "peer_network": "10.0.0.0/24"}}}}')