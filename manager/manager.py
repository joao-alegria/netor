import json
from messaging import Messaging
from threading import Thread

class VSMF(Thread):
    def __init__(self, vsiId, info):
        super().__init__()
        self.vsiId=vsiId
        # self.action=action
        self.info=info
        self.receivedData=set()
        self.received={}
        self.messaging=Messaging()
        self.messaging.consumeQueue("vsLCM_"+str(vsiId),self.vsCallback)

    def vsCallback(self, channel, method_frame, header_frame, body):
        print(" [x] Received %r" % body)
        data=json.loads(body)
        th=Thread(target=self.processAction, args=[data])
        th.start()

    def processAction(self, data):
        messaging=Messaging()
        self.receivedData.add(data["msgType"])
        self.received[data["msgType"]]=data
        if "placementInfo" in self.receivedData and "domainInfo" in self.receivedData and "tenantInfo" in self.receivedData:
            data=self.received["placementInfo"]["data"]
            data["name"]=self.info["data"]["name"]
            message={"action":"instantiateNS", "data":data}
            messaging.publish2Queue("vsDomain", json.dumps(message))
            statusUpdate={"vsiId":self.vsiId, "status":"instantiating"}
            messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))

    def run(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.messaging.startConsuming()