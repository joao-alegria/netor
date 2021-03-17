from rabbitmq.adaptor import Messaging
import json
from threading import Thread

class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.consumeExchange("vsLCM_Management",self.callback)
    
    def callback(self, channel, method_frame, header_frame, body):
        print(" [x] Received %r" % body)
        data=json.loads(body)
        #TODO meter logica num ficheiro separado
        if data["msgType"] == "createVSI":
            message={"msgType":"placementInfo", "data":{"nsId":"72f9e7d3-41d1-4dab-b6ae-bd1ee514bd93", "domainId":"osm"}}
            messaging.publish2Queue("vsLCM_"+str(data["vsiId"]), json.dumps(message))

    def run(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.messaging.startConsuming()