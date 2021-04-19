from rabbitmq.adaptor import Messaging
import json
from threading import Thread
from arbitrator import Arbitrator
import logging

class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.consumeExchange("vsLCM_Management",self.callback)
        # self.arbitrators={}
    
    def callback(self, channel, method_frame, header_frame, body):
        logging.info("Received Message {}".format(body))
        data=json.loads(body)

        if data["msgType"]=="createVSI":
            arbitrator=Arbitrator(data["vsiId"],data)
            # self.arbitrators[data["vsiId"]]=arbitrator
            arbitrator.start()
        # else:
        #     if data["vsiId"] in self.arbitrators:
        #         self.arbitrators[data["vsiId"]].newMessage(data)
        #     else:
        #         logging.warning("VSI Id not found: "+data["vsiId"])
        
    def run(self):
        logging.info('Started Consuming RabbitMQ Topics')
        self.messaging.startConsuming()