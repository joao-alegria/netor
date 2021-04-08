from rabbitmq.adaptor import Messaging
import json
from threading import Thread
from manager import newCSMF,newCsmfMessage
import logging

class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.consumeExchange("vsLCM_Management",self.callback)
        self.csmfs={}

    def callback(self, channel, method_frame, header_frame, body):
        logging.info("Received Message {}".format(body))
        data=json.loads(body)
        if data["msgType"]=="createVSI":
            newCSMF(data)
        else:
            newCsmfMessage(data)

    def run(self):
        logging.info('Started Consuming RabbitMQ Topics')
        self.messaging.startConsuming()