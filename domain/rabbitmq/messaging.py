from rabbitmq.adaptor import Messaging
import json
from threading import Thread
import db.persistance as persistance
import driver.osm as osm

class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.createQueue("vsDomain")
        self.messaging.consumeExchange("vsLCM_Management",self.callback)
        self.messaging.consumeQueue("vsDomain",self.myCallback)

    def myCallback(self, ch, method, properties, body):
        print(" Last Step - Received %r" % body)
        data=json.loads(body)
        #TODO colocar logica no service
        if data["msgType"] == "instantiateNs":
            domain=persistance.session.query(persistance.Domain).filter(persistance.Domain.domainId==data["data"]["domainId"]).first()
            osm.instantiateNs(domain.url, data["data"]["name"], data["data"]["nsId"], domain.vim)
        elif data["msgType"] == "instantiateNsi":
            return
        elif data["msgType"] == "deleteNs":
            return
        elif data["msgType"] == "deleteNsi":
            return
        elif data["msgType"] == "actionNs":
            return

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)
        data=json.loads(body)
        # messaging.consumeQueue("vsLCM_"+str(data["vsiId"]),simplecallback)
        if data["msgType"] == "createVSI":
            try:
                domainId=data["data"]["domainId"]
                domain=service.getDomain(domainId)
                message={"msgType":"domainInfo", "data":domain}
                self.messaging.publish2Queue("vsLCM_"+str(data["vsiId"]), json.dumps(message))
            except Exception as e:
                statusUpdate={"vsiId":self.vsiId, "status":"error", "msg":"Invalid domain."}
                messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))

    def run(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.messaging.startConsuming()