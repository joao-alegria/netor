from rabbitmq.adaptor import Messaging
import json
from threading import Thread
import arbitrator
import logging

class MessageReceiver(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.consumeExchange("vsLCM_Management",self.callback)
        self.arbitrators={}
        
    def callback(self, channel, method_frame, header_frame, body):
        logging.info("Received Message {}".format(body))
        data=json.loads(body)

        if data["msgType"]=="createVSI":
            self.newArbitrator(data)
        elif data["msgType"]=="removeVSI":
            self.tearDownArbitrator(data)
        # else:
        #     if data["vsiId"] in self.arbitrators:
        #         self.arbitrators[data["vsiId"]].newMessage(data)
        #     else:
        #         logging.warning("VSI Id not found: "+data["vsiId"])
    
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

    def newArbitrator(self,data):
        arb=arbitrator.Arbitrator(data["vsiId"], data)
        self.arbitrators[data["vsiId"]]=arb
        arb.start()

    def tearDownArbitrator(self,data):
        vsiId=str(data["vsiId"])
        if vsiId in self.arbitrators:
            self.arbitrators[vsiId].tearDown()
            del self.arbitrators[vsiId]
        else:
            logging.info("VSI Id not found during tearDown: "+str(vsiId))


        