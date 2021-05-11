import pytest
import redisHandler
import rabbitmq.adaptor
import arbitrator
import json

@pytest.fixture
def arbitratorMock(redisSet, rabbit):
    arb = arbitrator.Arbitrator("1",{})
    arb.start()
    yield arb
    arb.stop()


@pytest.fixture
def rabbit(monkeypatch, mocker):
    def mock_messaging(*args, **kwargs):
        return None
    monkeypatch.setattr(rabbitmq.adaptor.Messaging, "__init__", mock_messaging)

    def mock_messagingConsume(*args, **kwargs):
        return None
    monkeypatch.setattr(rabbitmq.adaptor.Messaging, "consumeQueue", mock_messagingConsume)

    # def mock_messagingPublish(*args, **kwargs):
    #     assert args==[]
    #     return None
    # monkeypatch.setattr(rabbitmq.adaptor.Messaging, "publish2Exchange", mock_messagingConsume)
    mocker.patch('rabbitmq.adaptor.Messaging.publish2Exchange')

@pytest.fixture
def badRedis(monkeypatch):
    def mock_redisGetEntireHash(*args, **kwargs):
        return {
            "domainInfo".encode("UTF-8"):json.dumps({"vsiId":"1","error":False, "message":"TestDomain"}),
            "tenantInfo".encode("UTF-8"):json.dumps({"vsiId":"1","error":False, "message":"TestTenant"}),
            "catalogueInfo".encode("UTF-8"):json.dumps({"vsiId":"1","error":True, "message":"TestCatalogue"})
            }
    monkeypatch.setattr(redisHandler, "getEntireHash", mock_redisGetEntireHash)

@pytest.fixture
def goodRedis(monkeypatch):
    def mock_redisGetEntireHash(*args, **kwargs):
        return {
            "domainInfo".encode("UTF-8"):json.dumps({"vsiId":"1","error":False, "message":"TestDomain", "data":["ITAV"]}),
            "tenantInfo".encode("UTF-8"):json.dumps({"vsiId": "1", "msgType": "tenantInfo", "data": {"username": "user", "group": "user", "vcpu": 100, "slas": [], "memory": 100, "storage": 100, "role": "TENANT"}, "error": False}),
            "catalogueInfo".encode("UTF-8"):json.dumps({"message": "Success", "vsiId": "1", "msgType": "catalogueInfo", "error": False, "data": {"vsd": {"tenant_id": "user", "associated_vsd_id": None, "domain_id": "ITAV", "vs_descriptor_id": "608ae08e063c52ff4d88f32f", "version": "1.0", "is_public": True, "nested_vsd_ids": {}, "service_constraints": [], "vs_blueprint_id": "608ae069063c52ff4d88f327", "name": "vsdTest", "sla": None, "management_type": "TENANT_MANAGED", "qos_parameters": {"peers": "2"}}, "vs_blueprint_info": {"vs_blueprint": {"urllc_service_category": None, "end_points": [], "inter_site": True, "parameters": [{"parameter_id": "peers", "parameter_type": "number", "applicability_field": "interdomain", "parameter_name": "Peers", "parameter_description": "#Peers"}], "version": "version_1", "blueprint_id": "608ae069063c52ff4d88f327", "service_sequence": [], "translation_rules": [{"nsd_version": "1.0", "input": [{"parameter_id": "peers", "max_value": 5, "min_value": 1}], "nsd_id": "interdomain-ns", "nst_id": "interdomain_e2e_nst", "blueprint_id": "608ae069063c52ff4d88f327", "nsd_info_id": None, "ns_instantiation_level_id": None, "ns_flavour_id": None}], "name": "vsb-test", "description": None, "atomic_components": [], "configurable_parameters": [], "application_metrics": [], "connectivity_services": [], "embb_service_category": "URBAN_MACRO", "slice_service_type": "EMBB"}, "on_boarded_nst_info_id": [], "on_boarded_mec_app_package_info_id": [], "on_boarded_vnf_package_info_id": [], "owner": None, "active_vsd_id": ["VsDescriptor object"], "vs_blueprint_id": "608ae069063c52ff4d88f327", "name": "vsb-test", "vs_blueprint_version": "version_1", "on_boarded_nsd_info_id": []}, "nsts": [{"nst_name": "Interdomain Slice", "nsst": [{"nst_name": "Interdomain Slice Subnet", "nsst": [], "nsd_version": "1.0", "geographical_area_info_list": [], "nst_provider": "ITAV", "nsd_id": "interdomain_slice_nsd", "nst_id": "interdomain_nsst", "nst_version": "1.0", "nst_service_profile": {"latency": 100, "sST": "EMBB", "resource_sharing_level": None, "max_number_of_UEs": 1000, "coverage_area_TA_list": [], "service_profile_id": "interdomain_profile", "uRLLC_perf_req": [], "availability": 100.0, "pLMN_id_list": [], "eMBB_perf_req": [{"user_density": 100, "activity_factor": None, "exp_data_rate_DL": None, "area_traffic_cap_DL": None, "area_traffic_cap_UL": None, "uE_speed": 10, "coverage": None, "exp_data_rate_uL": None}], "uE_mobility_level": None}, "nsst_type": "NONE", "nsst_ids": []}, {"nst_name": "Interdomain Slice Subnet", "nsst": [], "nsd_version": "1.0", "geographical_area_info_list": [], "nst_provider": "ITAV", "nsd_id": "interdomain_slice_nsd", "nst_id": "interdomain_nsst", "nst_version": "1.0", "nst_service_profile": {"latency": 100, "sST": "EMBB", "resource_sharing_level": None, "max_number_of_UEs": 1000, "coverage_area_TA_list": [], "service_profile_id": "interdomain_profile", "uRLLC_perf_req": [], "availability": 100.0, "pLMN_id_list": [], "eMBB_perf_req": [{"user_density": 100, "activity_factor": None, "exp_data_rate_DL": None, "area_traffic_cap_DL": None, "area_traffic_cap_UL": None, "uE_speed": 10, "coverage": None, "exp_data_rate_uL": None}], "uE_mobility_level": None}, "nsst_type": "NONE", "nsst_ids": []}], "nsd_version": "1.0", "geographical_area_info_list": [], "nst_provider": "ITAV", "nsd_id": None, "nst_id": "interdomain_e2e_nst", "nst_version": "1.0", "nst_service_profile": {"latency": 100, "sST": "EMBB", "resource_sharing_level": None, "max_number_of_UEs": 1000, "coverage_area_TA_list": [], "service_profile_id": "interdomain_profile", "uRLLC_perf_req": [], "availability": 100.0, "pLMN_id_list": [], "eMBB_perf_req": [{"user_density": 100, "activity_factor": None, "exp_data_rate_DL": None, "area_traffic_cap_DL": None, "area_traffic_cap_UL": None, "uE_speed": 10, "coverage": None, "exp_data_rate_uL": None}], "uE_mobility_level": None}, "nsst_type": "NONE", "nsst_ids": ["interdomain_nsst", "interdomain_nsst"]}], "vsb_actions": [{"action_name": "Add Tunnel Peer", "action_id": "addpeer", "parameters": [{"parameter_type": "STRING", "parameter_id": "peer_network", "parameter_name": "Peer Network", "parameter_default_value": "10.0.0.0/24"}], "blueprint_id": "608ae069063c52ff4d88f327"}, {"action_name": "Fetch Tunnel Peer Info", "action_id": "getvnfinfo", "parameters": [], "blueprint_id": "608ae069063c52ff4d88f327"}]}})
            }
    monkeypatch.setattr(redisHandler, "getEntireHash", mock_redisGetEntireHash)


@pytest.fixture
def nstRedis(monkeypatch):
    def mock_redisGetEntireHash(*args, **kwargs):
        return {
            "domainInfo".encode("UTF-8"):json.dumps({"vsiId":"1","error":False, "message":"TestDomain", "data":["ITAV"]}),
            "tenantInfo".encode("UTF-8"):json.dumps({"vsiId": "1", "msgType": "tenantInfo", "data": {"username": "user", "group": "user", "vcpu": 100, "slas": [], "memory": 100, "storage": 100, "role": "TENANT"}, "error": False}),
            "catalogueInfo".encode("UTF-8"):json.dumps({"message": "Success", "vsiId": "1", "msgType": "catalogueInfo", "error": False, "data": {"vsd": {"tenant_id": "user", "management_type": "TENANT_MANAGED", "name": "vsdTestNST", "associated_vsd_id": None, "domain_id": "ITAV", "vs_blueprint_id": "608c6caac91f86d903b997bf", "qos_parameters": {"peers": "2"}, "is_public": True, "service_constraints": [], "vs_descriptor_id": "608c6cc7c91f86d903b997c7", "sla": None, "nested_vsd_ids": {}, "version": "1.0"}, "vs_blueprint_info": {"vs_blueprint_version": "version_1", "vs_blueprint": {"inter_site": True, "end_points": [], "name": "vsb-testNST", "application_metrics": [], "connectivity_services": [], "configurable_parameters": [], "blueprint_id": "608c6caac91f86d903b997bf", "parameters": [{"applicability_field": "interdomain", "parameter_id": "peers", "parameter_name": "Peers", "parameter_type": "number", "parameter_description": "#Peers"}], "slice_service_type": "EMBB", "embb_service_category": "URBAN_MACRO", "translation_rules": [{"nsd_info_id": None, "input": [{"parameter_id": "peers", "max_value": 5, "min_value": 1}], "blueprint_id": "608c6caac91f86d903b997bf", "ns_flavour_id": None, "nsd_version": "1.0", "nst_id": "interdomain_e2e_nstNST", "nsd_id": None, "ns_instantiation_level_id": None}], "service_sequence": [], "urllc_service_category": None, "description": None, "atomic_components": [], "version": "version_1"}, "name": "vsb-testNST", "on_boarded_mec_app_package_info_id": [], "vs_blueprint_id": "608c6caac91f86d903b997bf", "on_boarded_vnf_package_info_id": [], "on_boarded_nst_info_id": [], "owner": None, "active_vsd_id": ["VsDescriptor object"], "on_boarded_nsd_info_id": []}, "nsts": [{"nst_id": "interdomain_e2e_nstNST", "nst_service_profile": {"uE_mobility_level": None, "coverage_area_TA_list": [], "sST": "EMBB", "eMBB_perf_req": [{"area_traffic_cap_DL": None, "uE_speed": 10, "area_traffic_cap_UL": None, "activity_factor": None, "coverage": None, "exp_data_rate_uL": None, "exp_data_rate_DL": None, "user_density": 100}], "availability": 100.0, "pLMN_id_list": [], "uRLLC_perf_req": [], "resource_sharing_level": None, "service_profile_id": "interdomain_profile", "latency": 100, "max_number_of_UEs": 1000}, "nst_version": "1.0", "nsd_version": "1.0", "nst_provider": "ITAV", "nst_name": "Interdomain Slice NST", "nsst_ids": ["interdomain_nst", "interdomain_nst"], "nsst_type": "NONE", "nsd_id": None, "geographical_area_info_list": []}], "vsb_actions": [{"blueprint_id": "608c6caac91f86d903b997bf", "parameters": [{"parameter_default_value": "10.0.0.0/24", "parameter_id": "peer_network", "parameter_name": "Peer Network", "parameter_type": "STRING"}], "action_id": "addpeer", "action_name": "Add Tunnel Peer"}, {"blueprint_id": "608c6caac91f86d903b997bf", "parameters": [], "action_id": "getvnfinfo", "action_name": "Fetch Tunnel Peer Info"}]}})
            }
    monkeypatch.setattr(redisHandler, "getEntireHash", mock_redisGetEntireHash)



@pytest.fixture
def redisSet(monkeypatch):
    def mock_redisSetValue(*args, **kwargs):
        return 0
    monkeypatch.setattr(redisHandler, "setKeyValue", mock_redisSetValue)

def test_propagatesError(arbitratorMock,badRedis):
    arbitratorMock.processEntitiesPlacement()
    rabbitmq.adaptor.Messaging.publish2Exchange.assert_called_with('vsLCM_1','{"vsiId": "1", "msgType": "placementInfo", "error": true, "message": "\\nCatalogue error: TestCatalogue"}')

def test_processesCorrectly(arbitratorMock,goodRedis):
    arbitratorMock.processEntitiesPlacement()
    rabbitmq.adaptor.Messaging.publish2Exchange.assert_called_with('vsLCM_1', '{"vsiId": "1", "msgType": "placementInfo", "error": false, "message": "Success", "data": [{"domainId": "ITAV", "sliceEnabled": false, "nsdId": "interdomain_slice_nsd"}, {"domainId": "ITAV", "sliceEnabled": false, "nsdId": "interdomain_slice_nsd"}]}')

def test_processesCorrectlyNST(arbitratorMock,nstRedis):
    arbitratorMock.processEntitiesPlacement()
    rabbitmq.adaptor.Messaging.publish2Exchange.assert_called_with('vsLCM_1', '{"vsiId": "1", "msgType": "placementInfo", "error": false, "message": "Success", "data": [{"domainId": "ITAV", "sliceEnabled": true, "nstId": "interdomain_nst"}, {"domainId": "ITAV", "sliceEnabled": true, "nstId": "interdomain_nst"}]}')