from rabbitmq.adaptor import Messaging
import json
from threading import Thread
import logging
import service

class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.createQueue("vsCoordinator")
        self.messaging.consumeQueue("vsCoordinator",self.callback)

    def callback(self, ch, method, properties, body):
        try:
            logging.info("Received Message {}".format(body))
            data=json.loads(body)
            if data["msgType"]=="statusUpdate":
                service.changeStatusVSI(data)
        except Exception as e:
            logging.error("Error while processing message: {}".format(body))

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
