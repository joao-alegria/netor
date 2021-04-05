import json
from messaging import Messaging
from threading import Thread

class Polling(Thread):

class CSMF(Thread):
    def __init__(self, vsiId, info):
        super().__init__()
        self.vsiId=vsiId
        # self.action=action
        self.info=info
        self.createVSI=True
        self.received={}
        self.messaging=Messaging()
        self.messaging.consumeQueue("vsLCM_"+str(vsiId),self.vsCallback)

    def vsCallback(self, channel, method_frame, header_frame, body):
        print(" [x] Received %r" % body)
        data=json.loads(body)
        th=Thread(target=self.processAction, args=[data])
        th.start()

    def processAction(self, data):
        if data["msgType"]=="modifyVSI":
            return
        elif data["msgType"]=="terminateVSI":
            return
        else:
            self.received[data["msgType"]]=data
            if self.createVSI and "placementInfo" in self.received.keys() and "domainInfo" in self.received.keys() and "tenantInfo" in self.received.keys():
                self.createVSI()
            return

    def createVSI(self):
        messaging=Messaging()

        placementData=self.received["placementInfo"]["data"]
        placementData["name"]=self.info["data"]["name"]
        message={"action":"instantiateNS", "data":placementData}
        messaging.publish2Queue("vsDomain", json.dumps(message))
        statusUpdate={"vsiId":self.vsiId, "status":"instantiating"}
        messaging.publish2Queue("vsCoordinator", json.dumps(statusUpdate))

        self.createVSI=False
        return

    def run(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.messaging.startConsuming()