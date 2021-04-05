from rabbitmq.adaptor import Messaging
from threading import Thread
import service
import json

class MessageReceiver(Thread):

    def __init__(self, app):
        super().__init__()
        self.app=app
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.consumeExchange("vsLCM_Management",self.callback)

    def callback(self, ch, method, properties, body):
        with self.app.app_context():
            print(" [x] Received %r" % body)
            data=json.loads(body)
            # messaging.consumeQueue("vsLCM_"+str(data["vsiId"]),simplecallback)
            if data["msgType"] == "createVSI":
                try:
                    tenantId=data["tenantId"]
                    tenant=service.getTenantById(tenantId)
                    message={"msgType":"tenantInfo", "data":tenant}
                    self.messaging.publish2Queue("vsLCM_"+str(data["vsiId"]), json.dumps(message))
                    service.addVsiToTenant(tenantId,data["vsiId"])
                except Exception as e:
                    statusUpdate={"vsiId":self.vsiId, "status":"error", "msg":"Invalid tenant."}
                    messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))


    def run(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.messaging.startConsuming()
