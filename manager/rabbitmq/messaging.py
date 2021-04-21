from rabbitmq.adaptor import Messaging
import json
from threading import Thread
from manager import newCSMF, tearDownCSMF
import logging

class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.consumeExchange("vsLCM_Management",self.callback)
        # self.csmfs={}

    def callback(self, channel, method_frame, header_frame, body):
        logging.info("Received Message {}".format(body))
        data=json.loads(body)
        if data["msgType"]=="createVSI":
            newCSMF(data)
        elif data["msgType"]=="removeVSI":
            tearDownCSMF(data)
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