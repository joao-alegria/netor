from rabbitmq.adaptor import Messaging
import json
from threading import Thread
import logging

class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.createQueue("vsCoordinator")
        self.messaging.consumeQueue("vsCoordinator",self.callback)

    def callback(self, ch, method, properties, body):
        logging.info("Received Message {}".format(body))
        # data=json.loads(body)

    def run(self):
        logging.info('Started Consuming RabbitMQ Topics')
        self.messaging.startConsuming()
