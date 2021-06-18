from rabbitmq.adaptor import Messaging
import json
from threading import Thread
import logging
import manager

class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.consumeExchange("vsLCM_Management",self.callback)
        self.pollingThread=manager.Polling()
        self.pollingThread.start()
        self.csmfs={}

    def callback(self, channel, method_frame, header_frame, body):
        logging.info("Received Message {}".format(body))
        # exchange = method_frame.exchange
        data=json.loads(body)
        # if exchange=="vsLCM_Management":
        if data["msgType"]=="createVSI":
            self.newCSMF(data)
        elif data["msgType"]=="removeVSI":
            self.tearDownCSMF(data)
        else:
            vsiId=data["vsiId"]
            if vsiId in self.csmfs:
                th=Thread(target=self.csmfs[vsiId].processAction, args=[data])
                th.start()
            else:
                logging.warning("VSI Id not found: "+data["vsiId"])
                
        # else:
        #     newCsmfMessage(data)

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
        self.pollingThread.stop()
    
    def newCSMF(self,data):
        csmf=manager.CSMF(data["vsiId"], data, self.pollingThread)
        self.csmfs[data["vsiId"]]=csmf
        # self.messaging.consumeQueue("managementQueue-vsLCM_"+str(data["vsiId"]), self.callback, ack=False)

    def tearDownCSMF(self,data):
        vsiId=str(data["vsiId"])
        if vsiId in self.csmfs:
            self.csmfs[vsiId].tearDown()
            del self.csmfs[vsiId]
        else:
            logging.info("VSI Id not found during tearDown: "+str(vsiId))

    # def newCsmfMessage(data):
    #     vsiId=int(data["vsiId"])
    #     if vsiId in csmfs:
    #         csmfs[vsiId].newMessage(data)
    #     else:
    #         logging.warning("VSI Id not found: "+str(vsiId))

    def newVnfInfo(self,data):
        vsiId=data["vsiId"]
        if vsiId in self.csmfs:
            self.csmfs[vsiId].interdomainHandler(data)
        else:
            logging.warning("VSI Id not found during newVnfInfo: "+str(vsiId))
            return {"error":True,"message": "Error: VSI Id not found during newVnfInfo: "+str(vsiId)}
        return {"error":False,"message": "Acknowledge"}
