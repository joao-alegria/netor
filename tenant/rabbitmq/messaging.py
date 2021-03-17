from rabbitmq.adaptor import Messaging
import json
from threading import Thread

class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.consumeExchange("vsLCM_Management",self.callback)

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        data=json.loads(body)
        # messaging.consumeQueue("vsLCM_"+str(data["vsiId"]),simplecallback)
        if data["msgType"] == "createVSI":
            message={"msgType":"tenantInfo", "data":"test"}
            self.messaging.publish2Queue("vsLCM_"+str(data["vsiId"]), json.dumps(message))

    def run(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.messaging.startConsuming()
