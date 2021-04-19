from rabbitmq.adaptor import Messaging
from threading import Thread
import service
import json
import logging

class MessageReceiver(Thread):

    def __init__(self, app):
        super().__init__()
        self.app=app
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.consumeExchange("vsLCM_Management",self.callback)

    def callback(self, channel, method, properties, body):
        with self.app.app_context():
            logging.info("Received Message {}".format(body))
            data=json.loads(body)
            # messaging.consumeQueue("vsLCM_"+str(data["vsiId"]),simplecallback)
            if data["msgType"] == "createVSI":
                try:
                    tenantId=data["tenantId"]
                    tenant=service.getTenantById(tenantId)
                    del tenant["password"]
                    del tenant["vsis"]
                    del tenant["vsds"]
                    message={"vsiId":data["vsiId"],"msgType":"tenantInfo", "data":tenant, "error":False}
                    self.messaging.publish2Exchange("vsLCM_"+str(data["vsiId"]), json.dumps(message))

                    # self.messaging.publish2Exchange("vsLCM_"+str(data["vsiId"]), json.dumps({"message":"Success", "vsiId":data["vsiId"] ,"msgType":"catalogueInfo","error":False,"data":{"vsd":{"is_public":True,"nested_vsd_ids":{},"vs_blueprint_id":"1","domain_id":"ITAV","version":"1.0","management_type":"TENANT_MANAGED","name":"vsdTest","qos_parameters":{"peers":"2"},"descriptor_id":"1","tenant_id":"admin"},"vs_blueprint_info":{"owner":"ITAV","vs_blueprint_id":"1","vs_blueprint_version":"version_1","name":"vsb-test","vs_blueprint":{"slice_service_type":"EMBB","translation_rules":[{"nst_id":"interdomain_e2e_nst","input":[{"max_value":5,"parameter_id":"peers","min_value":1}],"nsd_version":"1.0","nsd_id":"interdomain-ns","blueprint_id":"1"}],"parameters":[{"parameter_id":"peers","parameter_type":"number","applicability_field":"interdomain","parameter_name":"Peers","parameter_description":"#Peers"}],"version":"version_1","name":"vsb-test","inter_site":True,"blueprint_id":"1","configurable_parameters":["peers"]}},"nsts":[{"nst_version":"1.0","nsst_ids":["interdomain_nsst","interdomain_nsst"],"nsst_type":"EMBB","nst_service_profile":{"service_profile_id":"interdomain_profile","eMBB_perf_req":[{"user_density":100,"uE_speed":10}],"latency":100,"sST":"EMBB","max_number_of_UEs":1000,"availability":100},"nsd_version":"1.0","nst_id":"interdomain_e2e_nst","nst_provider":"ITAV","nst_name":"Interdomain Slice"},{"nst_version":"1.0","nsst_type":"EMBB","nst_service_profile":{"service_profile_id":"interdomain_profile","eMBB_perf_req":[{"user_density":100,"uE_speed":10}],"latency":100,"sST":"EMBB","max_number_of_UEs":1000,"availability":100},"nsd_version":"1.0","nst_id":"interdomain_nsst","nst_provider":"ITAV","nst_name":"Interdomain Slice Subnet","nsd_id":"interdomain_slice_nsd"}]}}))

                    service.addVsiToTenant(tenantId,data["vsiId"])
                except Exception as e:
                    message={"vsiId":data["vsiId"],"msgType":"tenantInfo", "error":True, "message":"Invalid Tenant Id. Error: "+str(e)}
                    self.messaging.publish2Exchange("vsLCM_"+str(self.vsiId), json.dumps(message))


    def run(self):
        logging.info('Started Consuming RabbitMQ Topics')
        self.messaging.startConsuming()
