from rabbitmq.adaptor import Messaging
import json
from threading import Thread
from db.persistance import persistance
from osmclient import client
from osmclient.common.exceptions import ClientException

class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.createQueue("vsDomain")
        self.messaging.consumeExchange("vsLCM_Management",self.callback)
        self.messaging.consumeQueue("vsDomain",self.myCallback)

    def myCallback(self, ch, method, properties, body):
        print(" Last Step - Pedido para instanciar %r" % body)
        data=json.loads(body)
        #TODO colocar logica no service
        domain=persistance.session.query(persistance.Domain).filter(persistance.Domain.domainId==data["data"]["domainId"]).first()
        print(domain.url)
        myClient = client.Client(host=domain.url)
        # myClient.ns.create("72f9e7d3-41d1-4dab-b6ae-bd1ee514bd93", "test", "microstack")
        myClient.ns.create(data["data"]["nsId"], data["data"]["name"], "microstack")

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        data=json.loads(body)
        # messaging.consumeQueue("vsLCM_"+str(data["vsiId"]),simplecallback)
        if data["msgType"] == "createVSI":
            message={"msgType":"domainInfo", "data":"test"}
            self.messaging.publish2Queue("vsLCM_"+str(data["vsiId"]), json.dumps(message))

    def run(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.messaging.startConsuming()