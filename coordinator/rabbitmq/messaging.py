from rabbitmq.adaptor import Messaging
import json
from threading import Thread

class MessageReceiver(Thread):

    def __init__(self):
        super().__init__()
        self.messaging=Messaging()
        self.messaging.createExchange("vsLCM_Management")
        self.messaging.createQueue("vsCoordinator")
        self.messaging.consumeQueue("vsCoordinator",self.callback)

    def callback(self, ch, method, properties, body):
        print(" [x] Received status update %r" % body)
        # data=json.loads(body)

    def run(self):
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.messaging.startConsuming()
