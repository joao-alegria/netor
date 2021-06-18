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
                    # self.messaging.publish2Exchange("vsLCM_"+str(data["vsiId"]), json.dumps(message))
                    self.messaging.publish2Exchange("vsLCM_Management", json.dumps(message))
                    service.addVsiToTenant(tenantId,data["vsiId"])
                except Exception as e:
                    message={"vsiId":data["vsiId"],"msgType":"tenantInfo", "error":True, "message":"Invalid Tenant Id. Error: "+str(e)}
                    # self.messaging.publish2Exchange("vsLCM_"+str(self.vsiId), json.dumps(message))
                    self.messaging.publish2Exchange("vsLCM_Management", json.dumps(message))
            elif data["msgType"]=="removeVSI":
                service.deleteVsiFromTenant(data["tenantId"], data["vsiId"])


    def stop(self):
        try:
            self.messaging.stopConsuming()
        except Exception as e:
            logging.error("Pika exception: "+str(e))

    def run(self):
        try:
            logging.info('Started Consuming RabbitMQ Topics')
            self.messaging.startConsuming()
        except Exception as e:
            logging.info("Stop consuming now!")
            logging.error("Pika exception: "+str(e))    
